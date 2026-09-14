import copy
import importlib.util
import json
from pathlib import Path
import unittest
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location('sync_project', ROOT / 'scripts/sync_project.py')
sync = importlib.util.module_from_spec(spec)
spec.loader.exec_module(sync)

class ProjectPlanTests(unittest.TestCase):
    def setUp(self):
        self.plan = json.loads((ROOT / 'planning/project.json').read_text())

    def test_complete_plan_and_dependencies(self):
        sync.validate_plan(self.plan)
        self.assertEqual(len(self.plan['issues']), 36)

    def test_wrong_repository_is_rejected(self):
        self.plan['repository'] = 'isqiwen/northstar-quant'
        with self.assertRaises(ValueError): sync.validate_plan(self.plan)

    def test_duplicate_issue_is_rejected(self):
        self.plan['issues'].append(copy.deepcopy(self.plan['issues'][0]))
        with self.assertRaises(ValueError): sync.validate_plan(self.plan)

    def test_missing_dependency_is_rejected(self):
        self.plan['issues'][0]['depends_on'] = [999999]
        with self.assertRaises(ValueError): sync.validate_plan(self.plan)

    def test_dependency_cycle_is_rejected(self):
        self.plan['issues'][0]['depends_on'] = [2]
        self.plan['issues'][1]['depends_on'] = [1]
        with self.assertRaises(ValueError): sync.validate_plan(self.plan)

    def test_invalid_option_is_rejected(self):
        self.plan['issues'][0]['fields']['Kind'] = 'Banana'
        with self.assertRaises(ValueError): sync.validate_plan(self.plan)

    def test_project_title_is_required_even_with_number(self):
        p = {'title':'Northstar Quant', 'number':1, 'closed':False}
        with self.assertRaises(ValueError): sync.select_project([p], 1)

    def test_duplicate_project_titles_need_number(self):
        p = {'title':sync.PROJECT_TITLE,'number':2,'closed':False}
        q = dict(p,number=3)
        with self.assertRaises(ValueError): sync.select_project([p,q],None)
        self.assertEqual(sync.select_project([p,q],3)['number'],3)

    def test_closed_project_is_not_selected(self):
        p={'title':sync.PROJECT_TITLE,'number':2,'closed':True}
        with self.assertRaises(ValueError): sync.select_project([p],2)

    def test_existing_fields_and_progress_are_preserved(self):
        desired={'Status':'Backlog','Phase':'Foundations','Target':'W01'}
        current={'Status':'In Progress','Phase':'Research'}
        self.assertEqual(sync.missing_updates(desired,current),{'Target':'W01'})

    def test_field_value_extraction(self):
        item={'fieldValues':{'nodes':[
            {'field':{'name':'Status'},'name':'Done'},
            {'field':{'name':'Target'},'text':'W02'},
            {'field':{'name':'Other'},'text':''},
        ],'pageInfo':{'hasNextPage':False}}}
        self.assertEqual(sync.field_values(item),{'Status':'Done','Target':'W02'})

    def test_partial_field_values_are_rejected(self):
        with self.assertRaises(RuntimeError):
            sync.field_values({'fieldValues':{'pageInfo':{'hasNextPage':True}}})

    def test_pagination_is_complete(self):
        pages=[{'x':{'nodes':[{'n':1}], 'pageInfo':{'hasNextPage':True,'endCursor':'A'}}},
               {'x':{'nodes':[{'n':2}], 'pageInfo':{'hasNextPage':False,'endCursor':'B'}}}]
        with patch.object(sync,'gql',side_effect=pages) as mock:
            self.assertEqual(sync.paged('query',('x',)),[{'n':1},{'n':2}])
            self.assertEqual(mock.call_args.kwargs['after'],'A')

    def test_repeated_cursor_is_rejected(self):
        p={'x':{'nodes':[], 'pageInfo':{'hasNextPage':True,'endCursor':'A'}}}
        with patch.object(sync,'gql',side_effect=[p,p]):
            with self.assertRaises(RuntimeError): sync.paged('query',('x',))

if __name__ == '__main__': unittest.main()
