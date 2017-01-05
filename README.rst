pyconau2017/website
===============

This is a fork of the lca2017/website repo.

Launchifying
------------

- create a virtualenv with python 2.7
- activate the virtualenv
- cd into the ``website`` directory
- ``pip install -r requirements.txt``
- ``python manage.py migrate``
- ``python manage.py loaddata ./fixtures/*``
- ``python manage.py runserver [YOUR PORT]``
