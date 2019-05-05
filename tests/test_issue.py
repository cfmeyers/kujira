from unittest.mock import MagicMock

from pytest import fixture

from kujira.issue import (
    IssueModel,
    UserModel,
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
            epic='Customer Experience (DS-100)',
        )
        assert issue.project == 'Death-Star'
        assert issue.assignee == 'Motti'
        assert issue.reporter == 'Vader'
        assert issue.summary == 'Your lack of faith'
        assert issue.description == 'I find your lack of faith disturbing.'
        assert issue.priority == '3'
        assert issue.issue_type == 'Task'
        assert issue.issue_id is None
        assert issue.epic == 'Customer Experience (DS-100)'
        assert issue.epic_key == 'DS-100'

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

    def test_it_parses_epic_keys(self, vader_issue):
        vader_issue.epic = 'Hello (D_123)'
        assert 'D_123' == vader_issue.epic_key

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

summary: Your lack of faith

assignee: Motti

reporter: Vader

epic: None

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
        issue = deserialize_issue_from_API(mock_api_issue, None)
        assert issue == vader_issue


class TestSerializeIssue:
    def test_it_takes_issue_and_returns_a_string_representation(self, vader_issue):
        expected = """\
project: Death-Star
issue_id: Death-Star-1610
issue_type: Task

summary: Your lack of faith

assignee: Motti

reporter: Vader

epic: None

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

summary: pending...

assignee: Vader

reporter: None

epic: None

priority: 3

description: |
    pending...
"""
        assert expected == make_new_issue_template(config)


@fixture
def vader_user():
    return UserModel(
        email='dvader@empire.com',
        name='dvader',
        key='dvader',
        display_name='Darth Vader',
    )


class TestUserModel:
    def test_it_has_user_fields(self, vader_user):
        assert 'dvader@empire.com' == vader_user.email
        assert 'dvader' == vader_user.key
        assert 'dvader' == vader_user.name
        assert 'Darth Vader' == vader_user.display_name

    def test_it_can_serialize_itself_from_api(self):
        api_user = MagicMock(
            emailAddress='dvader@empire.com',
            displayName='Darth Vader',
            key='dvader',
            name='dvader',
        )
        user = UserModel.from_API(api_user)
        assert 'dvader@empire.com' == user.email
        assert 'dvader' == user.key
        assert 'Darth Vader' == user.display_name

    def test_it_serializes_itself_to_string(self, vader_user):
        as_string = str(vader_user)
        assert '[dvader] [dvader] [Darth Vader] [dvader@empire.com]' == as_string

    def test_two_users_with_the_same_attributes_are_the_same(self, vader_user):
        vader_user_2 = UserModel(
            email='dvader@empire.com',
            name='dvader',
            key='dvader',
            display_name='Darth Vader',
        )

        assert vader_user == vader_user_2

    def test_it_deserializes_itself_from_string(self, vader_user):
        string_vader = '[dvader] [dvader] [Darth Vader] [dvader@empire.com]'
        assert vader_user == UserModel.from_string(string_vader)
