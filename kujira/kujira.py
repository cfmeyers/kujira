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
