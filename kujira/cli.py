# -*- coding: utf-8 -*-

"""Console script for kujira."""
import click

from kujira.kujira import (
    get_open_issues,
    get_conn,
    get_printable_issue,
    get_issue_by_key,
    transition_issue,
    read_config,
    create_new_issue,
    get_issues_for_status,
    get_printable_issue_brief,
    advance_issue,
    get_all_epics,
    associate_epic_to_issue,
    get_users,
)
from kujira.models.user import UserModel


@click.group()
def main(args=None):
    """Console script for kujira."""
    return 0


@main.command()
def mine():
    config = read_config()
    conn = get_conn(config)
    for issue in get_open_issues(conn):
        click.echo(get_printable_issue_brief(issue))


@main.command()
@click.argument('issue_key', type=str)
def fix_issue(issue_key):
    config = read_config()
    conn = get_conn(config)
    issue = get_issue_by_key(conn, issue_key)
    transition_issue(conn, issue, 'Reopen Issue')
    transition_issue(conn, issue, 'Start Progress')
    transition_issue(conn, issue, 'Pull Request')
    transition_issue(conn, issue, 'Ready For Deployment')
    transition_issue(conn, issue, 'Deployed')


@main.command()
@click.argument('issue_key', type=str)
def get_issue(issue_key):
    config = read_config()
    conn = get_conn(config)
    issue = get_issue_by_key(conn, issue_key)
    print(get_printable_issue(issue, conn))


@main.command()
@click.argument('issue_key', type=str)
def inspect(issue_key):
    config = read_config()
    conn = get_conn(config)
    issue = get_issue_by_key(conn, issue_key)
    breakpoint()


@main.command()
@click.argument('issue_key', type=str)
def advance(issue_key):
    config = read_config()
    conn = get_conn(config)
    issue = get_issue_by_key(conn, issue_key)
    result = advance_issue(conn, issue)
    if not result:
        msg = f'Failed to transition, issue still {issue.fields.status.name}'
    else:
        msg = f'Transitioned from {issue.fields.status.name} to {result}'
    click.echo(msg)


@main.command()
@click.argument('issue_key', type=str)
def rm(issue_key):
    config = read_config()
    conn = get_conn(config)
    issue = get_issue_by_key(conn, issue_key)
    issue.delete()


@main.command()
@click.argument('project_name', type=str)
def epics_for_project(project_name):
    config = read_config()
    conn = get_conn(config)
    for e in get_all_epics(conn, project_name):
        click.echo(f'{e.fields.summary} ({e.key})')


@main.command()
def get_all_users():
    config = read_config()
    conn = get_conn(config)
    for user in get_users(conn):
        click.echo(UserModel.from_API(user))


@main.command()
@click.argument('issue_key', type=str)
@click.argument('epic_key', type=str)
def add_epic_to_issue(issue_key, epic_key):
    config = read_config()
    conn = get_conn(config)
    issue = get_issue_by_key(conn, issue_key)
    try:
        epic_issue = get_issue_by_key(conn, epic_key)
    except Exception as e:
        click.echo(f'Could not find an epic with the key {epic_key}')
    try:
        associate_epic_to_issue(conn, issue, epic_issue)
        issue = get_issue_by_key(conn, issue_key)
        confirmed_epic_key = issue.fields.customfield_10910
        click.echo(f'Added epic {confirmed_epic_key} to {issue_key}')
    except Exception as e:
        breakpoint()
        click.echo(f'Could not add epic {epic_key} to {issue_key}')


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
    for issue in get_issues_for_status(conn, status):
        click.echo(get_printable_issue_brief(issue))


if __name__ == "__main__":
    main()
