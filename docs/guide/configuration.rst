Configuration
=============

Environment Variables
---------------------

RESTIC_REPOSITORY
~~~~~~~~~~~~~~~~~

Sets the restic repository path.

This is a standard environment variable
the ``restic`` command will read making it simple for
us to enter the container and use the restic command directly.

More about this value and supported backends:
https://restic.readthedocs.io/en/stable/030_preparing_a_new_repo.html

RESTIC_PASSWORD
~~~~~~~~~~~~~~~

Sets the password is used to encrypt/decrypt data.
Losing this password will make recovery impossible.

This is a standard environment variable the ``restic``
command will read making it simple for us to enter the
container running the command directly.

RESTIC_KEEP_DAILY
~~~~~~~~~~~~~~~~~

**Default value**: ``7``

How many daily snapshots (grouped by path) back in time we
want to keep. This is passed to restic in the
``forget --keep-daily`` option.

RESTIC_KEEP_WEEKLY
~~~~~~~~~~~~~~~~~~

**Default value**: ``4``

How many weeks back we should keep at least one snapshot
(grouped by path). This is passed to restic in the
``forget --keep-weekly`` option.

RESTIC_KEEP_MONTHLY
~~~~~~~~~~~~~~~~~~~

**Default value**: ``12``

How many months back we should keep at least on snapshot
(grouped by path). This is passed to restic in the
``forget --keep-monthly`` option.

The schedule parameters only accepts numeric values
and is validated when the container starts. Providing
values cron does not understand will stall all backup.

RESTIC_KEEP_YEARLY
~~~~~~~~~~~~~~~~~~

**Default value**: ``3``

How many years back we should keep at least one snapshot
(grouped by path). This is passed to restic in the
``forget --keep-yearly`` option.

CRON_SCHEDULE
~~~~~~~~~~~~~

**Default value**: ``0 2 * * *`` (daily at 02:00)

The cron schedule parameters. The crontab is generated when the
container starts from the ``CRON_SCHEDULE`` and ``CRON_COMMAND``
env variables.

.. code::

    ┌───────────── minute (0 - 59)
    │ ┌───────────── hour (0 - 23)
    │ │ ┌───────────── day of the month (1 - 31)
    │ │ │ ┌───────────── month (1 - 12)
    │ │ │ │ ┌───────────── day of the week (0 - 6) (Sunday to Saturday)
    │ │ │ │ │
    │ │ │ │ │
    │ │ │ │ │
    * * * * * command to execute

CRON_COMMAND
~~~~~~~~~~~~

**Default value**: ``source /env.sh && rcb backup > /proc/1/fd/1``

The command executed in the crontab. A single line is generated when
the container starts from the ``CRON_SCHEDULE`` and ``CRON_COMMAND``
environment variables.

The default command sources a dump of all env vars, runs the
backup command and directs output to pid 1 so it appears in
docker logs.

By default the crontab will look like this::

    0 2 * * * source /env.sh && rcb backup > /proc/1/fd/1

LOG_LEVEL
~~~~~~~~~

**Default value**: ``info``

Log level for the ``rcb`` command. Valid values are
``debug``, ``info``, ``warning``, ``error``.

EMAIL_HOST
~~~~~~~~~~

The email host to use.

Alerts can be tested using the ``rcb alerts`` command.
This will send a test message to all configured alert
backends.

EMAIL_PORT
~~~~~~~~~~

The port to connect to

Alerts can be tested using the ``rcb alerts`` command.
This will send a test message to all configured alert
backends.

EMAIL_HOST_USER
~~~~~~~~~~~~~~~

The user of the sender account

Alerts can be tested using the ``rcb alerts`` command.
This will send a test message to all configured alert
backends.

EMAIL_HOST_PASSWORD
~~~~~~~~~~~~~~~~~~~

The password for the sender account

Alerts can be tested using the ``rcb alerts`` command.
This will send a test message to all configured alert
backends.

EMAIL_SEND_TO
~~~~~~~~~~~~~

The email address to send alerts

Alerts can be tested using the ``rcb alerts`` command.
This will send a test message to all configured alert
backends.

DISCORD_WEBHOOK
~~~~~~~~~~~~~~~

The discord webhook url. And administrator can quickly set this up
by going to server settings in the discord client and create
a webhook that will post embedded messages to a specific channel.

The url usually looks like this: ``https://discordapp.com/api/webhooks/...```

DOCKER_BASE_URL
~~~~~~~~~~~~~~~

**Default value**: ``unix://tmp/docker.sock``

The location of the docker socket.

Compose Labels
--------------

A simple `include` and `exclude` filter is also available.

.. code:: yaml

    example:
      image: some_image
      labels:
        restic-compose-backup.volumes: true
        restic-compose-backup.volumes.include: "files,data"
      volumes:
        # Source don't match include filter. No backup.
        - media:/srv/media
        # Matches include filter
        - files:/srv/files
        - /srv/data:/srv/data

    volumes:
      media:
      files:

Exclude

.. code:: yaml

    example:
      image: some_image
      labels:
        restic-compose-backup.volumes: true
        restic-compose-backup.volumes.exclude: "media"
      volumes:
        # Excluded by filter
        - media:/srv/media
        # Backed up
        - files:/srv/files
        - /srv/data:/srv/data

    volumes:
      media:
      files:

Databases

Will dump databases directly into restic through stdin.
They will appear in restic as a separate snapshot with
path `/databases/<service_name>/dump.sql` or similar.
