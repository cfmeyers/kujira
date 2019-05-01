# -*- coding: utf-8 -*-

"""Console script for kujira."""
from datetime import datetime, timedelta
import sys
import click
from kujira.kujira import (
    get_open_issues,
    get_conn,
    get_printable_issue,
    get_issue_by_id,
    transition_issue,
    read_config,
    create_new_issue,
    get_issues_for_status,
    get_printable_issue_brief,
    advance_issue,
    get_all_epics,
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
        click.echo(get_printable_issue(issue))


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
def get_issue(issue_id):
    config = read_config()
    conn = get_conn(config)
    issue = get_issue_by_id(conn, issue_id)
    print(get_printable_issue(issue))


@main.command()
@click.argument('issue_id', type=str)
def inspect(issue_id):
    config = read_config()
    conn = get_conn(config)
    issue = get_issue_by_id(conn, issue_id)
    breakpoint()


@main.command()
@click.argument('issue_id', type=str)
def advance(issue_id):
    config = read_config()
    conn = get_conn(config)
    issue = get_issue_by_id(conn, issue_id)
    result = advance_issue(conn, issue)
    if not result:
        click.echo(f'Failed to transition, issue still {issue.fields.status.name}')
    else:
        click.echo(f'Transitioned from {issue.fields.status.name} to {result}')


@main.command()
@click.argument('issue_id', type=str)
def rm(issue_id):
    config = read_config()
    conn = get_conn(config)
    issue = get_issue_by_id(conn, issue_id)
    issue.delete()


@main.command()
@click.argument('project_name', type=str)
def epics_for_project(project_name):
    config = read_config()
    conn = get_conn(config)
    epic_issues = get_all_epics(conn, project_name)
    ids_and_summaries = [(i.fields.summary, i.id) for i in epic_issues]
    for issue in ids_and_summaries:
        click.echo(f'{issue[0]} ({issue[1]})')


@main.command()
def new():
    config = read_config()
    conn = get_conn(config)
    new_issue = create_new_issue(conn, config)
    click.echo(new_issue)


@main.command()
@click.argument('status', type=str)
def ls(status):
    config = read_config()
    conn = get_conn(config)
    issues = get_issues_for_status(conn, status)
    for issue in issues:
        click.echo(get_printable_issue_brief(issue))


if __name__ == "__main__":
    main()
