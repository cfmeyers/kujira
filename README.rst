======
kujira
======


.. image:: https://img.shields.io/pypi/v/kujira.svg
        :target: https://pypi.python.org/pypi/kujira

.. image:: https://img.shields.io/travis/cfmeyers/kujira.svg
        :target: https://travis-ci.org/cfmeyers/kujira

.. image:: https://readthedocs.org/projects/kujira/badge/?version=latest
        :target: https://kujira.readthedocs.io/en/latest/?badge=latest
        :alt: Documentation Status


.. image:: https://pyup.io/repos/github/cfmeyers/kujira/shield.svg
     :target: https://pyup.io/repos/github/cfmeyers/kujira/
     :alt: Updates



A set of scripts for managing Jira using jira-python


* Free software: MIT license
* Documentation: https://kujira.readthedocs.io.


Todo
--------

* make default statuses in jiraconfig
* add comments to ticket
* add ability to specify custom field for epics
* make json file for reading in transitions
* move issues into models directory
* move serialize-from-api function to IssueModel class method
* move serialize-from-string function to IssueModel class method
* add initial test for cli
* add date last updated to issue model
* add link to issue to IssueModel
* add ability to search for arbitrary tickets
* move current_issue functionality from python to shell script
* add ability to make a ticket for someone else



Credits
-------

This package was created with Cookiecutter_ and the `audreyr/cookiecutter-pypackage`_ project template.

.. _Cookiecutter: https://github.com/audreyr/cookiecutter
.. _`audreyr/cookiecutter-pypackage`: https://github.com/audreyr/cookiecutter-pypackage
