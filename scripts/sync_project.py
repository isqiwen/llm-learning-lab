#!/usr/bin/env python3
"""Populate one existing GitHub Project; default is read-only, writes require --apply.

Credentials stay in the user's gh session. Existing field values, issue states,
project visibility, views, and workflows are never overwritten by this tool.
"""
from __future__ import annotations

import argparse
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
REPOSITORY = "isqiwen/llm-learning-lab"
PROJECT_TITLE = "LLM Learning & Research"
PAGE_INFO = "pageInfo { hasNextPage endCursor }"
FIELD_FRAGMENT = """
... on ProjectV2Field { id name dataType }
... on ProjectV2IterationField { id name dataType }
... on ProjectV2SingleSelectField { id name dataType options { id name } }
"""
VALUE_FRAGMENT = """
... on ProjectV2ItemFieldSingleSelectValue {
 name field { ... on ProjectV2SingleSelectField { name } }
}
... on ProjectV2ItemFieldTextValue {
 text field { ... on ProjectV2Field { name } }
}
"""


def gh(*args: str, payload: dict[str, Any] | None = None) -> Any:
    env = dict(os.environ, GH_HOST="github.com", GH_PROMPT_DISABLED="1")
    proc = subprocess.run(
        ["gh", *args], input=json.dumps(payload) if payload is not None else None,
        capture_output=True, text=True, timeout=120, check=False, env=env,
    )
    if proc.returncode:
        raise RuntimeError(proc.stderr.strip() or "GitHub CLI failed.")
    return json.loads(proc.stdout) if proc.stdout.strip() else {}


def gql(query: str, **variables: Any) -> dict[str, Any]:
    result = gh("api", "graphql", "--input", "-",
                payload={"query": query, "variables": variables})
    if result.get("errors"):
        raise RuntimeError(json.dumps(result["errors"], ensure_ascii=False))
    if not isinstance(result.get("data"), dict):
        raise RuntimeError("GraphQL returned no data; check gh authentication and project scope.")
    return result["data"]


def paged(query: str, path: tuple[str, ...], **variables: Any) -> list[dict[str, Any]]:
    nodes: list[dict[str, Any]] = []
    cursor = None
    seen: set[str] = set()
    while True:
        obj: Any = gql(query, after=cursor, **variables)
        for part in path:
            obj = obj[part]
        nodes.extend(node for node in obj["nodes"] if node is not None)
        info = obj["pageInfo"]
        if not info["hasNextPage"]:
            return nodes
        cursor = info["endCursor"]
        if not cursor or cursor in seen:
            raise RuntimeError("Invalid pagination cursor; stopped rather than using partial data.")
        seen.add(cursor)


def validate_plan(plan: dict[str, Any]) -> None:
    if plan.get("repository") != REPOSITORY or plan.get("project_title") != PROJECT_TITLE:
        raise ValueError("Unexpected target. This script is scoped to llm-learning-lab only.")
    issues = plan["issues"]
    numbers = [x["issue"] for x in issues]
    if not numbers or any(type(n) is not int or n <= 0 for n in numbers):
        raise ValueError("Issue numbers must be positive integers.")
    if len(numbers) != len(set(numbers)):
        raise ValueError("Duplicate issue numbers in the plan.")
    specs = plan["fields"]
    required = {"Phase", "Kind", "Priority", "Effort", "Target"}
    if set(specs) != required:
        raise ValueError("Unexpected project field schema.")
    by_number = {x["issue"]: x for x in issues}
    for row in issues:
        if set(row["fields"]) != required:
            raise ValueError(f"Missing fields for #{row['issue']}.")
        for name, spec in specs.items():
            value = row["fields"][name]
            if not isinstance(value, str) or not value:
                raise ValueError(f"Empty/non-string {name} in #{row['issue']}.")
            if spec["type"] == "SINGLE_SELECT" and value not in spec["options"]:
                raise ValueError(f"Unknown {name} value: {value}")
        if row.get("parent") is not None and row["parent"] not in by_number:
            raise ValueError("Unknown parent issue.")
        if any(n not in by_number for n in row.get("depends_on", [])):
            raise ValueError("Unknown dependency.")
    visited: set[int] = set()
    visiting: set[int] = set()
    def visit(n: int) -> None:
        if n in visiting:
            raise ValueError("Dependency cycle in learning plan.")
        if n in visited:
            return
        visiting.add(n)
        for dep in by_number[n].get("depends_on", []):
            visit(dep)
        visiting.remove(n)
        visited.add(n)
    for number in numbers:
        visit(number)


def select_project(projects: list[dict[str, Any]], number: int | None) -> dict[str, Any]:
    matches = [p for p in projects if not p["closed"] and p["title"] == PROJECT_TITLE
               and (number is None or p["number"] == number)]
    if len(matches) != 1:
        raise ValueError("Expected exactly one open project with the exact title. "
                         "Inspect gh project list; use --project-number only to disambiguate.")
    return matches[0]


def field_values(item: dict[str, Any]) -> dict[str, str]:
    connection = item.get("fieldValues", {})
    if connection.get("pageInfo", {}).get("hasNextPage"):
        raise RuntimeError("More than 100 item field values; cannot safely fill blanks.")
    values = {}
    for value in connection.get("nodes", []):
        name = (value.get("field") or {}).get("name")
        data = value.get("text", value.get("name"))
        if name and data not in (None, ""):
            values[name] = data
    return values


def missing_updates(desired: dict[str, str], current: dict[str, str]) -> dict[str, str]:
    return {name: value for name, value in desired.items() if name not in current}


def run(plan: dict[str, Any], apply: bool, number: int | None) -> None:
    owner, repo = REPOSITORY.split("/")
    viewer = gql("query { viewer { login } }")["viewer"]["login"]
    if viewer != owner:
        raise RuntimeError(f"Authenticated as {viewer}; expected {owner}. No writes performed.")
    projects = paged("query($owner:String!,$after:String){user(login:$owner){"
                     "projectsV2(first:100,after:$after){nodes{id number title url closed}"
                     + PAGE_INFO + "}}}", ("user", "projectsV2"), owner=owner)
    project = select_project(projects, number)
    pid = project["id"]
    print(f"Target: {project['url']} ({project['title']})")
    issues = paged("query($owner:String!,$repo:String!,$after:String){"
                   "repository(owner:$owner,name:$repo){issues(first:100,after:$after,"
                   "states:[OPEN,CLOSED]){nodes{id number state}" + PAGE_INFO + "}}}",
                   ("repository", "issues"), owner=owner, repo=repo)
    issue_map = {i["number"]: i for i in issues}
    missing = [r["issue"] for r in plan["issues"] if r["issue"] not in issue_map]
    if missing:
        raise RuntimeError(f"Missing repository issues: {missing}. No writes performed.")
    def read_fields() -> dict[str, Any]:
        fields = paged("query($id:ID!,$after:String){node(id:$id){... on ProjectV2{"
                       "fields(first:100,after:$after){nodes{" + FIELD_FRAGMENT + "}"
                       + PAGE_INFO + "}}}}", ("node", "fields"), id=pid)
        return {f["name"]: f for f in fields if "name" in f}
    fields = read_fields()
    # Validate ALL existing fields before the first write. Never replace options/IDs.
    for name, spec in plan["fields"].items():
        if name not in fields:
            continue
        field = fields[name]
        if field.get("dataType") != spec["type"]:
            raise RuntimeError(f"Field {name} has a different type. Resolve manually; no writes performed.")
        if spec["type"] == "SINGLE_SELECT":
            absent = set(spec["options"]) - {o["name"] for o in field["options"]}
            if absent:
                raise RuntimeError(f"Add missing {name} options {sorted(absent)} in the UI first. "
                                   "Existing options are preserved; no writes performed.")
    items = paged("query($id:ID!,$after:String){node(id:$id){... on ProjectV2{"
                  "items(first:100,after:$after){nodes{id isArchived content{... on Issue{"
                  "number repository{nameWithOwner}}} fieldValues(first:100){nodes{"
                  + VALUE_FRAGMENT + "}" + PAGE_INFO + "}}" + PAGE_INFO + "}}}}",
                  ("node", "items"), id=pid)
    item_map = {}
    for item in items:
        content = item.get("content") or {}
        if (content.get("repository") or {}).get("nameWithOwner") == REPOSITORY:
            field_values(item)  # Refuse truncated data before any writes.
            item_map[content["number"]] = item
    for name, spec in plan["fields"].items():
        if name in fields:
            continue
        print(f"{'CREATE' if apply else 'WOULD CREATE'} field: {name}")
        if apply:
            args = ["project", "field-create", str(project["number"]), "--owner", owner,
                    "--name", name, "--data-type", spec["type"], "--format", "json"]
            if spec["type"] == "SINGLE_SELECT":
                args += ["--single-select-options", ",".join(spec["options"])]
            gh(*args)
    if apply:
        fields = read_fields()
    status_options = {o["name"]: o["id"] for o in fields.get("Status", {}).get("options", [])}
    for row in plan["issues"]:
        n = row["issue"]
        item = item_map.get(n)
        if item and item.get("isArchived"):
            print(f"KEEP archived item #{n}")
            continue
        if item is None:
            print(f"{'ADD' if apply else 'WOULD ADD'} issue #{n}")
            if apply:
                item = gql("mutation($input:AddProjectV2ItemByIdInput!){"
                           "addProjectV2ItemById(input:$input){item{id}}}",
                           input={"projectId": pid, "contentId": issue_map[n]["id"]})["addProjectV2ItemById"]["item"]
                # Refetch: workflows may already have set fields after add.
                item = gql("query($id:ID!){node(id:$id){... on ProjectV2Item{"
                           "id fieldValues(first:100){nodes{" + VALUE_FRAGMENT + "}"
                           + PAGE_INFO + "}}}}", id=item["id"])["node"]
        current = field_values(item or {})
        desired = dict(row["fields"])
        preferred = "Done" if issue_map[n]["state"] == "CLOSED" else row.get("initial_status", "Backlog")
        status = preferred if preferred in status_options else ("Todo" if preferred != "Done" and "Todo" in status_options else None)
        if status:
            desired["Status"] = status
        for name, value in missing_updates(desired, current).items():
            print(f"{'SET' if apply else 'WOULD SET'} #{n} {name}={value}")
            if not apply:
                continue
            field = fields[name]
            if field["dataType"] == "SINGLE_SELECT":
                options = {o["name"]: o["id"] for o in field["options"]}
                encoded = {"singleSelectOptionId": options[value]}
            else:
                encoded = {"text": value}
            gql("mutation($input:UpdateProjectV2ItemFieldValueInput!){"
                "updateProjectV2ItemFieldValue(input:$input){projectV2Item{id}}}",
                input={"projectId": pid, "itemId": item["id"], "fieldId": field["id"], "value": encoded})
    print("Completed additive sync." if apply else "Read-only preview complete. Use --apply to write.")
    print("Views, Status options, native sub-issues/dependencies and workflows were NOT changed.")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--apply", action="store_true", help="Perform additive writes; default only previews.")
    parser.add_argument("--validate-only", action="store_true", help="Validate the local plan without network or gh.")
    parser.add_argument("--project-number", type=int, help="Disambiguate projects; exact title is still required.")
    args = parser.parse_args()
    if args.apply and args.validate_only:
        parser.error("--apply and --validate-only are mutually exclusive")
    try:
        plan = json.loads((ROOT / "planning/project.json").read_text(encoding="utf-8"))
        validate_plan(plan)
        if args.validate_only:
            print(f"Valid plan: {len(plan['issues'])} issues; acyclic dependencies; target {REPOSITORY}.")
            return 0
        if not shutil.which("gh"):
            raise RuntimeError("Install GitHub CLI, then gh auth login and gh auth refresh -h github.com -s project.")
        run(plan, args.apply, args.project_number)
        return 0
    except (RuntimeError, ValueError, KeyError, OSError, subprocess.TimeoutExpired) as exc:
        print(f"ERROR: {exc}\nNo rollback was attempted. Inspect partial changes and rerun safely; "
              "do not paste tokens into chat.", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
