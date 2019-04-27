import yaml


class IssueModel:
    def __init__(
        self, project, assignee, reporter, summary, description, priority, issue_id=None
    ):
        self.project = project
        self.assignee = assignee
        self.reporter = reporter
        self.summary = summary
        self.description = description
        self.priority = priority
        self.issue_id = issue_id

    def __eq__(self, other):
        return (
            (self.project == other.project)
            and (self.assignee == other.assignee)
            and (self.reporter == other.reporter)
            and (self.summary == other.summary)
            and (self.description == other.description)
            and (self.priority == other.priority)
            and (self.issue_id == other.issue_id)
        )

    def __str__(self):
        return f"""\
project: {self.project}
issue_id: { self.issue_id }

summary: |
    {self.summary}

assignee: { self.assignee }

reporter: { self.reporter }

priority: { self.priority }

description: |
    {self.description}
"""

    def __repr__(self):
        return f"""\
IssueModel(project='{self.project}', assignee='{self.assignee}', reporter='{self.reporter}', summary='{self.summary}', priority='{self.priority}', issue_id='{self.issue_id}')"""


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
        )
    return issue


def serialize(issue):
    return str(issue)
