===========
PollScraper
===========


.. .. image:: https://img.shields.io/pypi/v/pollscraper.svg
..         :target: https://pypi.python.org/pypi/pollscraper

.. image:: https://github.com/AEJaspan/PollScraper/actions/workflows/python-app.yml/badge.svg
        :target: https://github.com/AEJaspan/PollScraper/actions/workflows/python-app.yml

.. image:: https://readthedocs.org/projects/pollscraper/badge/?version=latest
        :target: https://pollscraper.readthedocs.io/en/latest/?version=latest
        :alt: Documentation Status




A production-ready web scraping utility, built to monitor polling data hosted by the Economist data team.


Artifacts from the latest build can be downloaded in the `Actions tab <https://github.com/AEJaspan/PollScraper/actions/workflows/python-app.yml>`.


Setup
--------

.. code-block:: console

        $ python3.7 -m venv .venv
        $ source .venv/bin/activate
        $ pip install -r requirements_dev.txt
        $ python setup.py install


Testing
--------

.. code-block:: console

        $ make lint
        $ make test-all

or full testing and linting suite:

.. code-block:: console

        $ tox



Building documentation
-----------------------

.. code-block:: console

        $ make docs


Deployment
------------

.. code-block:: console

        $ bump2version patch # possible: major / minor / patch
        $ git push
        $ git push --tags


* Free software: MIT license
* Documentation: https://pollscraper.readthedocs.io.


Features
--------

* TODO

Credits
-------

This package was created with Cookiecutter_ and the `audreyr/cookiecutter-pypackage`_ project template.

.. _Cookiecutter: https://github.com/audreyr/cookiecutter
.. _`audreyr/cookiecutter-pypackage`: https://github.com/audreyr/cookiecutter-pypackage
