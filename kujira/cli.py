# -*- coding: utf-8 -*-

"""Console script for kujira."""
from datetime import datetime, timedelta
import sys
import click
from kujira.kujira import (
    get_open_issues,
    get_conn,
    get_issue_summary,
    get_issue_by_id,
    transition_issue,
    read_config,
    create_new_issue,
)


@click.group()
def main(args=None):
    """Console script for kujira."""
    return 0


@main.command()
def mine():
    config = read_config()
    conn = get_conn(config)
    issues = get_open_issues(conn)
    for issue in issues:
        click.echo(get_issue_summary(issue))


# <JIRA Project: key='XFL', name='Infralytics', id='14320'>


@main.command()
@click.argument('issue_id', type=str)
def fix_issue(issue_id):
    config = read_config()
    conn = get_conn(config)
    issue = get_issue_by_id(conn, issue_id)
    transition_issue(conn, issue, 'Reopen Issue')
    transition_issue(conn, issue, 'Start Progress')
    transition_issue(conn, issue, 'Pull Request')
    transition_issue(conn, issue, 'Ready For Deployment')
    transition_issue(conn, issue, 'Deployed')


@main.command()
@click.argument('issue_id', type=str)
def rm(issue_id):
    config = read_config()
    conn = get_conn(config)
    issue = get_issue_by_id(conn, issue_id)
    issue.delete()


@main.command()
def new():
    config = read_config()
    conn = get_conn(config)
    summary = 'Test jira issue for XFL'
    description = 'Just a test'
    new_issue = create_new_issue(conn, config, summary, description)
    click.echo(get_issue_summary(new_issue))


if __name__ == "__main__":
    main()
