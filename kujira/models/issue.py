import re

import dateutil.parser
import yaml


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
        updated_at,
        epic=None,
        issue_id=None,
        url=None,
    ):
        self.project = project
        self.issue_type = issue_type
        self.assignee = assignee
        self.reporter = reporter
        self.summary = summary
        self.description = description
        self.priority = priority
        self.updated_at = updated_at
        self.issue_id = issue_id
        self.epic = epic if epic else "None"
        self.url = url

    @classmethod
    def from_api(cls, api_issue, epic_tag):
        return cls(
            issue_id=api_issue.key,
            project=api_issue.fields.project.key,
            assignee=api_issue.fields.assignee.key,
            reporter=api_issue.fields.reporter.key,
            summary=api_issue.fields.summary,
            description=api_issue.fields.description,
            priority=api_issue.fields.priority.name,
            issue_type=api_issue.fields.issuetype.name,
            epic=epic_tag,
            updated_at=dateutil.parser.parse(api_issue.fields.updated),
            url=api_issue.permalink(),
        )

    @classmethod
    def from_file(cls, path_to_issue):
        with open(path_to_issue, "r") as f:
            data = yaml.safe_load(f)
            return cls(
                project=process_string(data["project"]),
                assignee=process_string(data["assignee"]),
                reporter=process_string(data["reporter"]),
                summary=process_string(data["summary"]),
                description=process_string(data["description"]),
                priority=process_string(str(data["priority"])),
                issue_id=process_string(data.get("issue_id")),
                issue_type=process_string(data.get("issue_type")),
                epic=process_string(data.get("epic")),
                updated_at=data.get("updated_at"),
                url=data.get("url"),
            )

    @property
    def epic_key(self):
        try:
            return re.findall(r"\(([\w-]+)\)", self.epic)[0]
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
            and (self.updated_at == other.updated_at)
            and (self.issue_id == other.issue_id)
            and (self.epic == other.epic)
            and (self.url == other.url)
        )

    def __str__(self):
        return f"""\
project: {self.project}
issue_id: { self.issue_id }
issue_type: { self.issue_type }
updated_at: { self.updated_at }
url: { self.url }

summary: {self.summary}

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
    return item.strip("\n").strip()


def serialize(issue):
    return str(issue)


def make_new_issue_template(config):
    issue = IssueModel(
        project=process_string(config.default_project),
        assignee=process_string(config.user_key),
        reporter="None",
        summary=process_string("pending..."),
        description=process_string("pending..."),
        priority=process_string(str(config.default_priority)),
        issue_id=process_string("None"),
        issue_type=process_string(config.default_issue_type),
        epic=process_string("None"),
        updated_at=process_string("None"),
    )
    return str(issue)


def get_updates(initial, edited):
    updates = {}
    if initial.description != edited.description:
        updates["description"] = edited.description
    # if initial.priority != edited.priority:
    #     updates['priority'] = edited.priority
    # if initial.assignee != edited.assignee:
    #     updates['assignee'] = edited.assignee
    # if initial.issue_type != edited.issue_type:
    #     updates['issuetype'] = edited.issue_type
    # if initial.project != edited.project:
    #     updates['project'] = edited.project
    return updates
