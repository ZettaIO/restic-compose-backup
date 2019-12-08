
# restic-compose-backup

![docs](https://readthedocs.org/projects/restic-compose-backup/badge/?version=latest)

Automatically detects and backs up volumes, mysql, mariadb and postgres databases in a docker-compose setup.
Currently tested with docker-ce 17, 18 and 19.

Backup using [restic] for a docker-compose setup.

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

Minimum configuration (env vars)

```bash
RESTIC_REPOSITORY
RESTIC_PASSWORD
```

More config options can be found in the [documentation].

Restic backend specific env vars : https://restic.readthedocs.io/en/stable/040_backup.html#environment-variables

### Compose Example

restic-backup.env

```env
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
  example:
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

## Contributing

Contributions are welcome regardless of experience level. Don't hesitate submitting issues, opening partial or completed pull requests.

[restic]: https://restic.net/
[documentation]: https://restic-compose-backup.readthedocs.io