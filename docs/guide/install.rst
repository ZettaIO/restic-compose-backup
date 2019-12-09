Introduction
============


Install
-------

restic-compose-backup is available at docker `docker hub`_.

.. code::

    docker pull restic-compose-backup

Optionally it can be built from source using the github_ repository.

.. code:: bash

    git clone https://github.com/ZettaIO/restic-compose-backup.git
    cd restic-compose-backup
    # Build and tag the image locally
    docker build src/ --tag restic-compose-backup

Bug reports and issues
----------------------

Please report bugs an issues on github_

Development setup
-----------------

Getting started with local development is fairly simple.
The github_ repository contains a simple ``docker-compose.yaml``

.. code:: bash

    docker-compose up -d
    # Enter the container in sh
    docker-compose run --rm backup sh

The dev compose setup maps in the source from the host
and the spawned backup container will inherit all
the volumes from the backup service ensuring code changes
propagates during development.

Set up a local venv and install the package in development mode::

    python -m venv .venv
    . .venv/bin/activate
    pip install -e ./src


.. _docker hub: https://hub.docker.com/r/zettaio/restic-compose-backup
.. _github: https://github.com/ZettaIO/restic-compose-backup
