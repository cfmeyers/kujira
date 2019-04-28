from unittest.mock import MagicMock

from pytest import fixture

from kujira.issue import (
    IssueModel,
    deserialize_issue_from_file,
    serialize,
    deserialize_issue_from_API,
    make_new_issue_template,
)

PATH_TO_VADER_FILE = 'tests/fixtures/darth_vader.jira_issue.yml'


@fixture
def vader_issue():
    return IssueModel(
        project='Death-Star',
        issue_type='Task',
        assignee='Motti',
        reporter='Vader',
        summary='Your lack of faith',
        description='I find your lack of faith disturbing.',
        priority='3',
        issue_id='Death-Star-1610',
    )


class TestIssue:
    def test_it_has_all_necessary_fields(self):
        issue = IssueModel(
            project='Death-Star',
            issue_type='Task',
            assignee='Motti',
            reporter='Vader',
            summary='Your lack of faith',
            description='I find your lack of faith disturbing.',
            priority='3',
        )
        assert issue.project == 'Death-Star'
        assert issue.assignee == 'Motti'
        assert issue.reporter == 'Vader'
        assert issue.summary == 'Your lack of faith'
        assert issue.description == 'I find your lack of faith disturbing.'
        assert issue.priority == '3'
        assert issue.issue_type == 'Task'
        assert issue.issue_id is None

    def test_two_issues_are_equal_if_their_attributes_are_equal(self):
        first_issue = IssueModel(
            project='Death-Star',
            issue_type='Task',
            assignee='Motti',
            reporter='Vader',
            summary='Your lack of faith',
            description='I find your lack of faith disturbing.',
            priority='3',
        )

        second_issue = IssueModel(
            project='Death-Star',
            issue_type='Task',
            assignee='Motti',
            reporter='Vader',
            summary='Your lack of faith',
            description='I find your lack of faith disturbing.',
            priority='3',
        )

        assert first_issue == second_issue

    def test_two_issues_are_not_equal_if_at_least_one_of_their_attributes_are_not_equal(
        self
    ):
        first_issue = IssueModel(
            project='Death-Star',
            issue_type='Task',
            assignee='Motti',
            reporter='Vader',
            summary='Your lack of faith',
            description='I find your lack of faith disturbing.',
            priority='3',
        )

        second_issue = IssueModel(
            project='SOMETHING DIFFERENT',
            issue_type=first_issue.issue_type,
            assignee=first_issue.assignee,
            reporter=first_issue.reporter,
            summary=first_issue.summary,
            description=first_issue.description,
            priority=first_issue.priority,
        )

        assert first_issue != second_issue

    def test_it_has_a_str_representation(self, vader_issue):
        expected = """\
project: Death-Star
issue_id: Death-Star-1610
issue_type: Task

summary: |
    Your lack of faith

assignee: Motti

reporter: Vader

priority: 3

description: |
    I find your lack of faith disturbing.
"""
        assert expected == str(vader_issue)


class TestDeserializeIssueFromFile:
    def test_it_reads_yaml_file_and_returns_issue_model(self, vader_issue):
        issue = deserialize_issue_from_file(PATH_TO_VADER_FILE)
        assert issue == vader_issue


class TestDeserializeIssueFromAPI:
    def test_it_reads_API_object_and_returns_issue_model(self, vader_issue):
        mock_api_issue = MagicMock(key='Death-Star-1610')
        mock_api_issue.fields.project.key = 'Death-Star'
        mock_api_issue.fields.assignee.key = 'Motti'
        mock_api_issue.fields.reporter.key = 'Vader'
        mock_api_issue.fields.summary = 'Your lack of faith'
        mock_api_issue.fields.description = 'I find your lack of faith disturbing.'
        mock_api_issue.fields.priority.name = '3'
        mock_api_issue.fields.issuetype.name = 'Task'
        issue = deserialize_issue_from_API(mock_api_issue)
        assert issue == vader_issue


class TestSerializeIssue:
    def test_it_takes_issue_and_returns_a_string_representation(self, vader_issue):
        expected = """\
project: Death-Star
issue_id: Death-Star-1610
issue_type: Task

summary: |
    Your lack of faith

assignee: Motti

reporter: Vader

priority: 3

description: |
    I find your lack of faith disturbing.
"""
        assert expected == serialize(vader_issue)


class TestMakeNewIssueTemplate:
    def test_it(self):
        config = MagicMock(
            user='Vader',
            default_project='Death-Star',
            default_issue_type='Task',
            user_key='Vader',
            default_priority=3,
        )
        expected = """\
project: Death-Star
issue_id: None
issue_type: Task

summary: |
    pending...

assignee: Vader

reporter: None

priority: 3

description: |
    pending...
"""
        assert expected == make_new_issue_template(config)
