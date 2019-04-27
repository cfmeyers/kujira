# -*- coding: utf-8 -*-

"""Main module."""
from collections import namedtuple
import configparser
import os

from jira import JIRA

Config = namedtuple(
    'Config', 'user api_key server_url default_project default_issue_type'
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
    )


def get_conn(config):
    config = read_config()
    options = {'server': config.server_url}

    return JIRA(options, basic_auth=(config.user, config.api_key))


def get_open_issues(conn):
    return conn.search_issues(
        'resolution = unresolved and assignee=currentuser() ORDER BY created'
    )


def get_issue_by_id(conn, id):
    return conn.issue(id)


def transition_issue(conn, issue, transition_name):
    transitions = conn.transitions(issue)
    for tns in transitions:
        if tns['name'] == transition_name:
            reopen_id = tns['id']
            conn.transition_issue(issue, reopen_id)
            return True
    return False


def get_issue_summary(issue):
    return f'{issue.key}: {issue.fields.summary}'


def create_new_issue(
    conn, config, summary, description, issue_type=None, project_name=None
):
    if project_name is None:
        project_name = config.default_project
    if issue_type is None:
        issue_type = config.default_issue_type

    new_issue = conn.create_issue(
        project=project_name,
        summary=summary,
        description=description,
        issuetype={'name': issue_type},
    )
    return new_issue
