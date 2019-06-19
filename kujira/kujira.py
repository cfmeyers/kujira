# -*- coding: utf-8 -*-

"""Main module."""
from collections import namedtuple
import configparser
import os

from jira import JIRA

from kujira.models.issue import make_new_issue_template, IssueModel, get_updates
from kujira.edit import edit

Config = namedtuple(
    'Config',
    'user api_key server_url default_project default_issue_type default_priority user_key',
)

ISSUE_TYPES = (
    'Epic',
    'Bug',
    'Task',
    'Story',
    'Subtask',
    'Incident',
    'Service request',
    'Change',
    'Problem',
)


def read_config(config_path='~/.jira/config.ini'):
    cfg = configparser.ConfigParser()
    cfg.read(os.path.expanduser(config_path))
    return Config(
        user=cfg['Jira']['user'],
        api_key=cfg['Jira']['api_key'],
        server_url=cfg['Jira']['server_url'],
        default_project=cfg['Jira']['default_project'],
        default_issue_type=cfg['Jira']['default_issue_type'],
        default_priority=cfg['Jira']['default_priority'],
        user_key=cfg['Jira']['user_key'],
    )


def get_conn(config):
    config = read_config()
    options = {'server': config.server_url}

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


def get_users(conn, query='%'):
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
        conn, 'resolution = unresolved and assignee=currentuser() ORDER BY created'
    )


def get_all_epics(conn, project_name='Infralytics'):
    yield from get_issues(conn, f'issuetype="Epic" AND project="{project_name}"')


def get_issues_for_status(conn, status):
    query = f'assignee=currentuser() and status="{status}" ORDER BY created'
    yield from get_issues(conn, query)


def get_issue_by_key(conn, id):
    return conn.issue(id)


NEXT_ACTION = {
    'Backlog': 'Start Progress',
    'To Do': 'In Progress',
    'In Progress': 'Code Review',
    'Code Review': 'Ready For Deployment',
    'Ready For Deployment': 'Done',
    'Resolved': 'Deployed',
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
        if tns['name'] == transition_name:
            reopen_id = tns['id']
            conn.transition_issue(issue, reopen_id)
            return transition_name
    return False


# issue.fields.comment.comments[0].body
def get_epic_tag(epic_issue):
    return f'{epic_issue.fields.summary} ({epic_issue.key})'


def get_printable_issue(issue, conn):
    try:
        epic_key = issue.fields.customfield_10910
        epic_issue = get_issue_by_key(conn, epic_key)
        epic_tag = get_epic_tag(epic_issue)
    except:
        epic_issue = None
    issue_model = IssueModel.from_api(issue, epic_tag)
    return issue_model


def get_printable_issue_brief(issue):
    issue_model = IssueModel.from_api(issue, None)
    updated = issue_model.updated_at.date()
    return f'{issue_model.issue_id} | {issue_model.summary} ({updated})'


def update_current_issue(issue):
    with open(os.path.expanduser('~/.jira/current_issue'), 'w') as f:
        f.write(get_printable_issue_brief(issue) + '\n')


def associate_epic_to_issue(conn, issue, epic_issue):
    return conn.add_issues_to_epic(epic_issue.id, [issue.key])


def edit_issue(conn, issue_key):
    api_issue = get_issue_by_key(conn, issue_key)
    issue = IssueModel.from_api(api_issue, None)
    edited_issue = edit(str(issue))
    updates = get_updates(issue, edited_issue)
    api_issue.update(**updates)


# [~accountid:557058:e3520510-e28a-421b-8f92-10f7211b6947] check
def create_new_issue(conn, config):
    issue_template = make_new_issue_template(config)
    issue = edit(issue_template)
    if issue.summary == 'pending...':
        print('Need to fill out summary.  Issue uncreated.')
        return
    print(str(issue))
    new_issue = conn.create_issue(
        project=issue.project,
        summary=issue.summary,
        description=issue.description,
        issuetype={'name': issue.issue_type},
        assignee={'name': issue.assignee},
    )
    update_current_issue(new_issue)
    try:
        epic_issue = get_issue_by_key(conn, issue.epic_key)
        val = associate_epic_to_issue(conn, new_issue, epic_issue)
    except Exception as exc:
        pass
    return new_issue
