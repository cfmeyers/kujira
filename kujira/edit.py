"""
Inspired by https://github.com/fmoo/python-editor/blob/master/editor.py by Peter Ruibal
"""
import os
import subprocess
from tempfile import NamedTemporaryFile

from kujira.issue import deserialize_issue_from_file


def get_editor():
    editor = os.environ.get('VISUAL')
    if not editor:
        editor = os.environ.get('EDITOR')
    if not editor:
        editor = 'vim'
    return editor


def edit(template):
    editor_name = get_editor()
    temp_file = NamedTemporaryFile(suffix='.jira_issue.yml')
    with open(temp_file.name, 'w') as f:
        f.write(template)

    args = [editor_name, temp_file.name]

    proc = subprocess.Popen(args, close_fds=True, stdout=None)
    proc.communicate()
    return deserialize_issue_from_file(temp_file.name)
