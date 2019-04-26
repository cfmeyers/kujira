# -*- coding: utf-8 -*-

"""Console script for kujira."""
import sys
import click
from kujira.kujira import get_open_issues, get_conn


@click.command()
def main(args=None):
    """Console script for kujira."""
    conn = get_conn()
    issues = get_open_issues(conn)
    for issue in issues:
        click.echo(issue.fields.summary)
    # click.echo("Replace this message by putting your code into " "kujira.cli.main")
    # click.echo("See click documentation at http://click.pocoo.org/")
    return 0


if __name__ == "__main__":
    main()
