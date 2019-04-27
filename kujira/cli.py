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
)


@click.group()
def main(args=None):
    """Console script for kujira."""
    return 0


@main.command()
def mine():
    conn = get_conn()
    issues = get_open_issues(conn)
    for issue in issues:
        click.echo(get_issue_summary(issue))


@main.command()
@click.argument('issue_id', type=str)
def fix_issue(issue_id):
    conn = get_conn()
    issue = get_issue_by_id(conn, issue_id)
    transition_issue(conn, issue, 'Reopen Issue')
    transition_issue(conn, issue, 'Start Progress')
    transition_issue(conn, issue, 'Pull Request')
    transition_issue(conn, issue, 'Ready For Deployment')
    transition_issue(conn, issue, 'Deployed')


if __name__ == "__main__":
    main()
