# GitHub Project 管理、权限与同步

目标仓库：`isqiwen/llm-learning-lab`。目标 Project 名：`LLM Learning & Research`。不使用量化项目的 Project #1；学习 Project 编号从 GitHub 查询，不能猜。

## 为什么“我授权”仍可能无法直接写

有三个独立层次：本人同意修改；GitHub 凭据具备对应资源权限；当前工具有执行该操作的接口。前两者不能凭空产生第三者。

本次会话能写仓库文件与 Issues，但当前提供的连接动作没有 Projects 操作或通用 GraphQL 写入口。GitHub 自身有 Projects GraphQL API；问题不是 GitHub 不支持，也不是要求用户重复口头授权。仓库 admin/push 权限不能证明个人 Projects 可写。

本机 `gh` 的 OAuth 授权属于本机凭据，不会自动复制到这个对话。不要把 PAT、`gh auth token` 输出、SSH 私钥或登录 cookie 发到聊天或公开仓库。本脚本只调用用户已经授权的 gh，不读取/输出原始令牌。

官方参考：[Projects API](https://docs.github.com/en/issues/planning-and-tracking-with-projects/automating-your-project/using-the-api-to-manage-projects)、[gh project](https://cli.github.com/manual/gh_project)、[gh auth refresh](https://cli.github.com/manual/gh_auth_refresh)。

## 本机安全配置

```bash
# 已有 gh 就不必重复安装
brew install gh

# 尚未登录时执行；已有登录先 gh auth status 检查
# gh auth login --hostname github.com --web

gh auth status
gh auth refresh --hostname github.com --scopes project
gh project list --owner isqiwen

# 首次获取仓库
gh repo clone isqiwen/llm-learning-lab
cd llm-learning-lab

python3 scripts/sync_project.py --validate-only
python3 scripts/sync_project.py          # 只读预览，不修改 GitHub
python3 scripts/sync_project.py --apply  # 确认后才写入
```

已 clone 时在原目录 `git pull --ff-only`，不要重复创建目录。`project` 是 CLI 文档列出的 Project 操作 scope；这份脚本会进一步检查当前登录身份必须为 isqiwen。若使用环境变量提供的 token，`gh auth refresh` 不会修改该 token 的权限，应由本人在本地更换合适的凭据，而非发到聊天。

## 脚本能做与不能做

会分页查找同名且未关闭的 Project；重名必须显式 `--project-number N`，且仍验证标题。读取完整仓库 Issues，校验计划中的每个编号。创建缺少的 Phase/Kind/Priority/Effort/Target 字段，将现有 Issues 加入 Project，仅填空值。已有字段类型或选项不兼容时停止，避免重建字段造成数据丢失。

不会：创建/删除 Project、删除/归档条目、改变可见性、覆盖已有字段或 Status、修改 Issue 内容/状态、创建原生父子/阻塞关系、配置 Views/工作流。已有归档条目保持归档。中途失败不作破坏性回滚，可以检查后重跑；不要与他人并发批量编辑同一 Project。

默认 Status 选项仍只有 Todo/In Progress/Done 时，Ready/Backlog 初始化回退到 Todo；已经存在的 Status 一律保留。因此脚本不是持续状态同步器。Issue 关闭后自动变 Done 需要在 Project 工作流中另行启用。

## 字段方案

| 字段 | 值 / 含义 |
|---|---|
| Status | 建议 Backlog / Ready / In Progress / Review / Done；使用内置字段，不新建同名字段 |
| Phase | Planning / Foundations / Deep Learning / Transformers / Pretraining / Post-training / LLM Systems / Reasoning & Agents / Research |
| Kind | Epic / Learning / Implementation / Experiment / Evaluation / Research / Operations |
| Priority | P0 阶段关键产物；P1 重要配套；P2 选修/后续；P3 想法。优先级不等于当前就绪 |
| Effort | S ≤4h，M 约4–12h，L 约12–24h，XL 应拆分或作为阶段/跨周工作包；估计须按实绩修正 |
| Target | 相对学习周或阶段窗口，例如 W01、W15-W26；不是日历截止日期 |

使用 **Kind** 表示自定义工作分类，避免把计划中的分类与 GitHub 自带 Type 混为同一个字段。早期 Issues 的 Type 文本是初版描述；新增任务与模板统一用 Kind，初始化映射以 planning/project.json 为准。

不默认增加十几个字段。实际需要时间轴时，再增加 Start date/Target date 并由本人确认日期；不要用 Target 文本冒充时间轴日期。

## 建议手动配置的 Views

| View | 布局与筛选 |
|---|---|
| Roadmap | Table，按 Phase 分组；看阶段与依赖。需要日历时间轴时再切 Roadmap layout |
| Execution | Board，按 Status 分列；排除 Kind=Epic |
| Current | Table，只显示 Ready/In Progress/Review；默认 Todo 工作流下自行挑选当前任务 |
| Experiments | Table，只看 Experiment/Evaluation/Research |
| Systems | Table，Phase=LLM Systems |

建议工作流：新条目初始 Todo/Backlog、Issue 关闭变 Done、重开回 Todo；配置后用一个测试任务验证，不默认宣称已启用。对仓库的 auto-add 只覆盖新匹配项的行为需按实际 UI 验证，初始历史 Issues 由脚本导入更明确。

## 日常执行与事实来源

Issue 保存验收与讨论；Project 保存实时状态；ROADMAP 定义范围；planning/project.json 只是可审核的初始化/依赖计划；PROGRESS 只记录证据已通过的成果。不要同时维护三份“完成百分比”。

Epic 是 #2–#9，不与子任务一起计完成率；它们目前不是 GitHub 原生 Milestones。文档中的 Parent/Depends on 是计划关系，除非另外配置，不会自动成为 GitHub 原生 Sub-issues/Dependencies。

Ready 需前置能力与资源具备；In Progress 最多两个；Review 必须附证据；Done 需要本人确认掌握/实验完成。学习者尚未开始时，只把 #22 选为下一步，不把所有 P0 都拖进 In Progress。

每周使用 templates/weekly-review.md 复盘；不自动安排提醒或后台训练。需要持续自动同步时，另行配置受限凭据与受审核的工作流，不让公开 PR 或不可信代码接触 Project token。
