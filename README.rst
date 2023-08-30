===========
PollScraper
===========


.. .. image:: https://img.shields.io/pypi/v/pollscraper.svg
..         :target: https://pypi.python.org/pypi/pollscraper

.. image:: https://github.com/AEJaspan/PollScraper/actions/workflows/python-app.yml/badge.svg
        :target: https://github.com/AEJaspan/PollScraper/actions/workflows/python-app.yml
        :alt: Continuous Integration Pipeline

.. image:: https://github.com/AEJaspan/PollScraper/actions/workflows/CDPipeline.yml/badge.svg
        :target: https://github.com/AEJaspan/PollScraper/actions/workflows/CDPipeline.yml
        :alt: Continuous Deployment Pipeline

.. image:: https://readthedocs.org/projects/pollscraper/badge/?version=latest
        :target: https://pollscraper.readthedocs.io/en/latest/?version=latest
        :alt: Documentation Status




A production-ready web scraping utility, built to monitor polling data hosted by the Economist data team.

Artifacts from the latest build can be downloaded in the `Actions tab <https://github.com/AEJaspan/PollScraper/actions/workflows/python-app.yml>`_.

Artifacts from the latest daily run can be downloaded in the `Actions tab <https://github.com/AEJaspan/PollScraper/actions/workflows/CDPipeline.yml>`_.

The build pipeline is also run as a cron job that executes at 17:30 daily, so these artifacts also reflect the most recent poll results.


Setup
--------

.. code-block:: console

        $ python3.8 -m venv .venv
        $ source .venv/bin/activate
        $ pip install -r requirements_dev.txt

.. $ python setup.py install



Run Pipeline
----------------

.. code-block:: console

        $ # For information on pollscraper argument:
        $ pollscraper --help
        $ # To scrape polls, and calculate trends:
        $ pollscraper --url https://cdn-dev.economistdatateam.com/jobs/pds/code-test/index.html --results_dir data --quiet


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

TODO
--------

.. |ss| raw:: html

   <strike>

.. |se| raw:: html

   </strike>
* |ss| Separation of Concerns - separate CI and CD pipelines |se|
* |ss| Add separate badges for each new pipeline |se|
* |ss| Parameterize the HTTP requests via Click |se|
* |ss| Tidy up documentation, remove stale references such as PyPi |se|

Credits
-------

This package was created with Cookiecutter_ and the `audreyr/cookiecutter-pypackage`_ project template.

.. _Cookiecutter: https://github.com/audreyr/cookiecutter
.. _`audreyr/cookiecutter-pypackage`: https://github.com/audreyr/cookiecutter-pypackage
