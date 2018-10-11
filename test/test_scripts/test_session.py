"""Unit tests for module /scripts/init/session.py."""
from datetime import datetime
import unittest
from scripts.session import update_session_status
from scripts import utils


class TestSession(unittest.TestCase):
    """Unit tests for class Session."""

    @classmethod
    def setUpClass(cls):
        """Execute this before the tests."""
        pass

    @staticmethod
    def get_test_case_name():
        """Generate unique name for unit test case."""
        test_case_name = 'test ' + datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")
        return test_case_name

    def test_update_session_status(self):
        """Unit tests for method update_session_status."""

        # Create test indicator group
        test_case_name = TestSession.get_test_case_name()
        mutation_create_indicator_group = '''mutation{createIndicatorGroup(input:{indicatorGroup:{name:"test_case_name"}}){indicatorGroup{id}}}'''
        mutation_create_indicator_group = mutation_create_indicator_group.replace('test_case_name', str(test_case_name))  # Use replace() instead of format() because of curly braces
        indicator_group = utils.execute_graphql_request(mutation_create_indicator_group)
        indicator_group_id = indicator_group['data']['createIndicatorGroup']['indicatorGroup']['id']

        # Create test indicator
        mutation_create_indicator = '''mutation{createIndicator(input:{indicator:{name:"test_case_name",flagActive:true,indicatorTypeId:1,indicatorGroupId:indicator_group_id}}){indicator{id}}}'''
        mutation_create_indicator = mutation_create_indicator.replace('test_case_name', str(test_case_name))  # Use replace() instead of format() because of curly braces
        mutation_create_indicator = mutation_create_indicator.replace('indicator_group_id', str(indicator_group_id))  # Use replace() instead of format() because of curly braces
        indicator = utils.execute_graphql_request(mutation_create_indicator)
        indicator_id = indicator['data']['createIndicator']['indicator']['id']

        # Create test batch
        mutation_create_batch = '''mutation{createBatch(input:{batch:{indicatorGroupId:indicator_group_id,status:"Pending"}}){batch{id}}}'''
        mutation_create_batch = mutation_create_batch.replace('indicator_group_id', str(indicator_group_id))  # Use replace() instead of format() because of curly braces
        batch = utils.execute_graphql_request(mutation_create_batch)
        batch_id = batch['data']['createBatch']['batch']['id']

        # Create test session
        mutation_create_session = '''mutation{createSession(input:{session:{indicatorId:indicator_id,batchId:batch_id,status:"Pending"}}){session{id}}}'''
        mutation_create_session = mutation_create_session.replace('indicator_id', str(indicator_id))  # Use replace() instead of format() because of curly braces
        mutation_create_session = mutation_create_session.replace('batch_id', str(batch_id))  # Use replace() instead of format() because of curly braces
        session = utils.execute_graphql_request(mutation_create_session)
        session_id = session['data']['createSession']['session']['id']

        # Update test session status
        data = update_session_status(session_id, 'Running')
        session_status = data['data']['updateSessionById']['session']['status']

        # Assert batch status is Running
        self.assertEqual(session_status, 'Running')

    @classmethod
    def tearDownClass(cls):
        """Execute this at the end of the tests."""
        pass


if __name__ == '__main__':
    unittest.main()
