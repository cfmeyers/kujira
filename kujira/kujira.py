# -*- coding: utf-8 -*-

"""Main module."""
import configparser
import os
import sys
from collections import namedtuple

from jira import JIRA

from kujira.edit import edit
from kujira.models.issue import IssueModel, get_updates, make_new_issue_template

Config = namedtuple(
    "Config",
    "user api_key server_url default_project default_issue_type default_priority account_id",
)

ISSUE_TYPES = (
    "Epic",
    "Bug",
    "Task",
    "Story",
    "Subtask",
    "Incident",
    "Service request",
    "Change",
    "Problem",
)


def read_config(config_path="~/.jira/config.ini"):
    cfg = configparser.ConfigParser()
    cfg.read(os.path.expanduser(config_path))
    return Config(
        user=cfg["Jira"]["user"],
        api_key=cfg["Jira"]["api_key"],
        server_url=cfg["Jira"]["server_url"],
        default_project=cfg["Jira"]["default_project"],
        default_issue_type=cfg["Jira"]["default_issue_type"],
        default_priority=cfg["Jira"]["default_priority"],
        account_id=cfg["Jira"]["account_id"],
    )


def get_conn(config):
    config = read_config()
    options = {"server": config.server_url}

    return JIRA(options, basic_auth=(config.user, config.api_key))


def get_issues(conn, query):
    maxResults = 50
    startAt = 0
    issues = conn.search_issues(query, startAt=startAt, maxResults=maxResults)
    while len(issues) > 0:
        for issue in issues:
            yield issue
        startAt += maxResults
        issues = conn.search_issues(query, startAt=startAt, maxResults=maxResults)


def get_users(conn, query="%"):
    maxResults = 1000
    startAt = 0
    users = conn.search_users(query, startAt=startAt, maxResults=maxResults)
    while len(users) > 0:
        for user in users:
            yield user
        startAt += maxResults
        users = conn.search_users(query, startAt=startAt, maxResults=maxResults)


def get_open_issues(conn):
    yield from get_issues(
        conn, "resolution = unresolved and assignee=currentuser() ORDER BY created"
    )


def get_all_epics(conn, project_name=None):
    if project_name is None:
        config = read_config()
        project_name = config.default_project
    yield from get_issues(conn, f'issuetype="Epic" AND project="{project_name}"')


def get_issues_for_status(conn, status):
    query = f'assignee=currentuser() and status="{status}" ORDER BY created'
    yield from get_issues(conn, query)


def get_issue_by_key(conn, id):
    return conn.issue(id)


# NEXT_ACTION = {
#     "Backlog": "Start Progress",
#     "To Do": "In Progress",
#     "In Progress": "Code Review",
#     "Code Review": "Ready For Deployment",
#     "Ready For Deployment": "Done",
#     "Resolved": "Deployed",
# }
NEXT_ACTION = {
    "Backlog": "In Progress",
    "In Progress": "In Review",
    "In Review": "Done",
}


def advance_issue(conn, issue):
    status = issue.fields.status.name
    transition_name = NEXT_ACTION.get(status)
    if transition_name:
        return transition_issue(conn, issue, transition_name)
    else:
        return False


def transition_issue(conn, issue, transition_name):
    transitions = conn.transitions(issue)
    for tns in transitions:
        if tns["name"] == transition_name:
            reopen_id = tns["id"]
            conn.transition_issue(issue, reopen_id)
            return transition_name
    return False


# issue.fields.comment.comments[0].body
def get_epic_tag(epic_issue):
    return f"{epic_issue.fields.summary} ({epic_issue.key})"


def get_printable_issue(issue, conn):
    try:
        epic_key = issue.fields.customfield_10910
        epic_issue = get_issue_by_key(conn, epic_key)
        epic_tag = get_epic_tag(epic_issue)
    except:
        epic_issue = None
        epic_tag = None
    issue_model = IssueModel.from_api(issue, epic_tag)
    return issue_model


def get_printable_issue_brief(issue):
    try:
        issue_model = IssueModel.from_api(issue, None)
    except Exception as e:
        print(e, file=sys.stderr)
        return None
    updated = issue_model.updated_at.date()
    return f"{issue_model.issue_id} | {issue_model.summary} ({updated})"


def update_current_issue(issue):
    print("Updating current issue")
    with open(os.path.expanduser("~/.jira/current_issue"), "w") as f:
        f.write(get_printable_issue_brief(issue) + "\n")


def edit_issue(conn, issue_key):
    api_issue = get_issue_by_key(conn, issue_key)
    issue = IssueModel.from_api(api_issue, None)
    edited_issue = edit(str(issue))
    updates = get_updates(issue, edited_issue)
    api_issue.update(**updates)


def print_issue_fields(issue):
    for key, value in issue.fields.__dict__.items():
        if value:
            print(f"{key}: {value}")


def get_current_sprint(conn):
    board_id = 137
    sprints = [
        s
        for s in conn.sprints(board_id)
        if s.name
        not in (
            "Icebox",
            "After COVID-19",
            "Data Eng Groomed Tickets",
            "Data Eng External Requests",
        )
        and "Data" in s.name
    ]
    return sprints[-1]


def create_new_issue(conn, config):
    issue_template = make_new_issue_template(config)
    issue = edit(issue_template)
    if issue.summary == "pending...":
        print("Need to fill out summary.  Issue uncreated.")
        return
    print(str(issue))

    print("Creating new issue")
    new_issue = conn.create_issue(
        project=issue.project,
        summary=issue.summary,
        description=issue.description,
        issuetype={"name": issue.issue_type},
        assignee={"accountId": config.account_id},
    )
    print("New issue created")
    update_current_issue(new_issue)
    try:

        epic_issue = get_issue_by_key(conn, issue.epic_key)
        if epic_issue:
            print(f"The epic issue is {epic_issue}")
            new_issue.update(fields={"parent": {"id": epic_issue.id}})
        else:
            print("No epic associated with ticket")
    except Exception as exc:
        print(exc)
        print("Failed to update issue with epic")
    return new_issue
