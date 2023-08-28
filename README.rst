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


Artefacts from the latest build can be downloaded in the `Actions tab <https://github.com/AEJaspan/PollScraper/actions/workflows/python-app.yml>`_.

The build pipeline is also run as a cron job that executes at 17:30 daily, so these artefacts also reflect the most recent poll results.


Setup
--------

.. code-block:: console

        $ python3.7 -m venv .venv
        $ source .venv/bin/activate
        $ pip install -r requirements_dev.txt

.. $ python setup.py install


Testing
--------

Full testing and linting suite:

.. code-block:: console

        $ tox



Building documentation
-----------------------

.. code-block:: console

        $ make servedocs


Deployment
------------

.. code-block:: console

        $ bumpversion --current-version <current_version> minor # possible: major / minor / patch
        $ git push
        $ git push --tags


* Free software: MIT license
* Documentation: https://pollscraper.readthedocs.io.



Credits
-------

This package was created with Cookiecutter_ and the `audreyr/cookiecutter-pypackage`_ project template.

.. _Cookiecutter: https://github.com/audreyr/cookiecutter
.. _`audreyr/cookiecutter-pypackage`: https://github.com/audreyr/cookiecutter-pypackage
