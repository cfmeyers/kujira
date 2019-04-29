# -*- coding: utf-8 -*-

"""Main module."""
from collections import namedtuple
import configparser
import os

from jira import JIRA

from kujira.issue import (
    deserialize_issue_from_API,
    make_new_issue_template,
    deserialize_issue_from_file,
)
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


def read_config(config_path='~/.jira_config.ini'):
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


def get_open_issues(conn):
    return conn.search_issues(
        'resolution = unresolved and assignee=currentuser() ORDER BY created'
    )


def get_all_epics(conn, project_name='Infralytics'):
    return conn.search_issues(f'issuetype="Epic" AND project="{project_name}"')


def get_issues_for_status(conn, status):
    query = f'assignee=currentuser() and status="{status}" ORDER BY created'
    return conn.search_issues(query)


def get_issue_by_id(conn, id):
    return conn.issue(id)


NEXT_ACTION = {
    'In Progress': 'Code Review',
    'Code Review': 'Ready For Deployment',
    'Ready For Deployment': 'Deployed',
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
            return True
    return False


def get_printable_issue(issue):
    issue_model = deserialize_issue_from_API(issue)
    return issue_model


def get_printable_issue_brief(issue):
    issue_model = deserialize_issue_from_API(issue)
    return f'{issue_model.issue_id} | {issue_model.summary}'


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
    return new_issue
