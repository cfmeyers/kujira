from pytest import fixture

from kujira.issue import IssueModel, deserialize_issue_from_file


PATH_TO_VADER_FILE = 'tests/fixtures/darth_vader.jira_issue.yml'


@fixture
def vader_issue():
    return IssueModel(
        project='Death-Star',
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
        assert issue.issue_id is None

    def test_two_issues_are_equal_if_their_attributes_are_equal(self):
        first_issue = IssueModel(
            project='Death-Star',
            assignee='Motti',
            reporter='Vader',
            summary='Your lack of faith',
            description='I find your lack of faith disturbing.',
            priority='3',
        )

        second_issue = IssueModel(
            project='Death-Star',
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
            assignee='Motti',
            reporter='Vader',
            summary='Your lack of faith',
            description='I find your lack of faith disturbing.',
            priority='3',
        )

        second_issue = IssueModel(
            project='SOMETHING DIFFERENT',
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

summary: |
    Your lack of faith

assignee: Motti

reporter: Vader

priority: 3

description: |
    I find your lack of faith disturbing.
"""
        assert expected == str(vader_issue)


class TestDeserializeIssue:
    def test_wired(self, vader_issue):
        issue = deserialize_issue_from_file(PATH_TO_VADER_FILE)
        assert issue == vader_issue
