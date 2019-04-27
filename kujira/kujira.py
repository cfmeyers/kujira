# -*- coding: utf-8 -*-

"""Main module."""
from collections import namedtuple
import configparser
import os

from jira import JIRA

Config = namedtuple('Config', 'user api_key server_url')


def read_config(config_path='~/.jira_config.ini'):
    cfg = configparser.ConfigParser()
    cfg.read(os.path.expanduser(config_path))
    return Config(
        user=cfg['Jira']['user'],
        api_key=cfg['Jira']['api_key'],
        server_url=cfg['Jira']['server_url'],
    )


def get_conn():
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
