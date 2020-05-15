
# restic-compose-backup

![docs](https://readthedocs.org/projects/restic-compose-backup/badge/?version=latest)

Backup using [restic] for a docker-compose setup.
Currently tested with docker-ce 17, 18 and 19.

* [restic-compose-backup Documentation](https://restic-compose-backup.readthedocs.io)
* [restic-compose-backup on Github](https://github.com/ZettaIO/restic-compose-backup)
* [restic-compose-backup on Docker Hub](https://hub.docker.com/r/zettaio/restic-compose-backup)

Features:

* Backs up docker volumes or host binds
* Backs up postgres, mariadb and mysql databases
* Notifications over mail/smtp or Discord webhooks

Please report issus on [github](https://github.com/ZettaIO/restic-compose-backup/issues).

## Install

```bash
docker pull zettaio/restic-compose-backup
```

## Configuration (env vars)

Minimum configuration

```bash
RESTIC_REPOSITORY
RESTIC_PASSWORD
```

More config options can be found in the [documentation].

Restic backend specific env vars : https://restic.readthedocs.io/en/stable/040_backup.html#environment-variables

## Compose Example

We simply control what should be backed up by adding
labels to our containers. More details are covered
in the [documentation].

restic-backup.env

```bash
RESTIC_REPOSITORY=<whatever backend restic supports>
RESTIC_PASSWORD=hopefullyasecturepw
# snapshot prune rules
RESTIC_KEEP_DAILY=7
RESTIC_KEEP_WEEKLY=4
RESTIC_KEEP_MONTHLY=12
RESTIC_KEEP_YEARLY=3
# Cron schedule. Run every day at 1am
CRON_SCHEDULE="0 1 * * *"
```

docker-compose.yaml

```yaml
version: '3'
services:
  # The backup service
  backup:
    image: zettaio/restic-compose-backup:<version>
    env_file:
      - restic-backup.env
    volumes:
      # We need to communicate with docker
      - /var/run/docker.sock:/tmp/docker.sock:ro
      # Persistent storage of restic cache (greatly speeds up all restic operations)
      - cache:/cache
  web:
    image: some_image
    labels:
      # Enables backup of the volumes below
      restic-compose-backup.volumes: true
    volumes:
      - media:/srv/media
      - /srv/files:/srv/files
  mariadb:
    image: mariadb:10
    labels:
      # Enables backup of this database
      restic-compose-backup.mariadb: true
    env_file:
      mariadb-credentials.env
    volumes:
      - mysqldata:/var/lib/mysql
  mysql:
    image: mysql:5
    labels:
      # Enables backup of this database
      restic-compose-backup.mysql: true
    env_file:
      mysql-credentials.env
    volumes:
      - mysqldata:/var/lib/mysql

  postgres:
    image: postgres
    labels:
      # Enables backup of this database
      restic-compose-backup.postgres: true
    env_file:
      postgres-credentials.env
    volumes:
      - pgdata:/var/lib/postgresql/data

volumes:
  media:
  mysqldata:
  mariadbdata:
  pgdata:
  cache:
```

## The `rcb` command

Everything is controlled using the `rcb` command.
After configuring backup with labels and restarted
the affected services we can quickly view the
result using the `status` subcommand.

```bash
$ docker-compose run --rm backup rcb status
INFO: Status for compose project 'myproject'
INFO: Repository: '<restic repository>'
INFO: Backup currently running?: False
INFO: --------------- Detected Config ---------------
INFO: service: mysql
INFO:  - mysql (is_ready=True)
INFO: service: mariadb
INFO:  - mariadb (is_ready=True)
INFO: service: postgres
INFO:  - postgres (is_ready=True)
INFO: service: web
INFO:  - volume: media
INFO:  - volume: /srv/files
```

The `status` subcommand lists what will be backed up and
even pings the database services checking their availability.
The `restic` command can also be used directly in the container.

More `rcb` commands can be found in the [documentation].

## Running Tests

```bash
pip install -e ./src/
pip install -r src/tests/requirements.txt
tox
```

## Building Docs

```bash
pip install -r docs/requirements.txt
python src/setup.py build_sphinx
```

# Local dev setup

The git repository contains a simple local setup for development

```bash
# Create an overlay network to link the compose project and stack
docker network create --driver overlay --attachable global
# Start the compose project
docker-compose up -d
# Deploy the stack
docker stack deploy -c swarm-stack.yml test
```

In dev we should ideally start the backup container manually

```bash
docker-compose run --rm backup sh
# pip install the package in the container in editable mode to auto sync changes from host source
pip3 install -e .
```

Remember to enable swarm mode with `docker swarm init/join` and disable swarm
mode with `docker swarm leave --force` when needed in development (single node setup).

## Contributing

Contributions are welcome regardless of experience level.
Don't hesitate submitting issues, opening partial or completed pull requests.

[restic]: https://restic.net/
[documentation]: https://restic-compose-backup.readthedocs.io

---
This project is sponsored by [zetta.io](https://www.zetta.io)

[![Zetta.IO](https://raw.githubusercontent.com/ZettaIO/restic-compose-backup/master/.github/logo.png)](https://www.zetta.io)
