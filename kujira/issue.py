import yaml
import re


class IssueModel:
    def __init__(
        self,
        project,
        issue_type,
        assignee,
        reporter,
        summary,
        description,
        priority,
        epic=None,
        issue_id=None,
    ):
        self.project = project
        self.issue_type = issue_type
        self.assignee = assignee
        self.reporter = reporter
        self.summary = summary
        self.description = description
        self.priority = priority
        self.issue_id = issue_id
        self.epic = epic if epic else 'None'

    @property
    def epic_id(self):
        try:
            return re.findall(r'\((\d+)\)', self.epic)[0]
        except:
            return None

    def __eq__(self, other):
        return (
            (self.project == other.project)
            and (self.issue_type == other.issue_type)
            and (self.assignee == other.assignee)
            and (self.reporter == other.reporter)
            and (self.summary == other.summary)
            and (self.description == other.description)
            and (self.priority == other.priority)
            and (self.issue_id == other.issue_id)
            and (self.epic == other.epic)
        )

    def __str__(self):
        return f"""\
project: {self.project}
issue_id: { self.issue_id }
issue_type: { self.issue_type }

summary: |
    {self.summary}

assignee: { self.assignee }

reporter: { self.reporter }

epic: { self.epic }

priority: { self.priority }

description: |
    {self.description}
"""

    def __repr__(self):
        return f"""\
IssueModel(project='{self.project}', issue_type='{self.issue_type}', assignee='{self.assignee}', reporter='{self.reporter}', summary='{self.summary}', priority='{self.priority}', issue_id='{self.issue_id}', epic='{self.epic}')"""


def process_string(item):
    return item.strip('\n').strip()


def deserialize_issue_from_file(path_to_issue):
    with open(path_to_issue, 'r') as f:
        data = yaml.safe_load(f)
        issue = IssueModel(
            project=process_string(data['project']),
            assignee=process_string(data['assignee']),
            reporter=process_string(data['reporter']),
            summary=process_string(data['summary']),
            description=process_string(data['description']),
            priority=process_string(str(data['priority'])),
            issue_id=process_string(data.get('issue_id')),
            issue_type=process_string(data.get('issue_type')),
            epic=process_string(data.get('epic')),
        )
    return issue


def deserialize_issue_from_API(jira_issue):
    return IssueModel(
        issue_id=jira_issue.key,
        project=jira_issue.fields.project.key,
        assignee=jira_issue.fields.assignee.key,
        reporter=jira_issue.fields.reporter.key,
        summary=jira_issue.fields.summary,
        description=jira_issue.fields.description,
        priority=jira_issue.fields.priority.name,
        issue_type=jira_issue.fields.issuetype.name,
    )


def serialize(issue):
    return str(issue)


def make_new_issue_template(config):
    issue = IssueModel(
        project=process_string(config.default_project),
        assignee=process_string(config.user_key),
        reporter='None',
        summary=process_string('pending...'),
        description=process_string('pending...'),
        priority=process_string(str(config.default_priority)),
        issue_id=process_string('None'),
        issue_type=process_string(config.default_issue_type),
        epic=process_string('None'),
    )
    return str(issue)
