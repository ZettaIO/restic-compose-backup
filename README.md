
# restic-compose-backup

![docs](https://readthedocs.org/projects/restic-compose-backup/badge/?version=latest)

Backup using https://restic.net/ for a docker-compose setup.

* [restic-compose-backup Documentation](https://restic-compose-backup.readthedocs.io)
* [restic-compose-backup on Github](https://github.com/ZettaIO/restic-compose-backup)
* [restic-compose-backup on Docker Hub](https://hub.docker.com/r/zettaio/restic-compose-backup)

Features:

* Back up docker volumes or host binds
* Back up mariadb postgres
* Back up mariadb databases
* Back up mysql databases
* Notifications over mail/smtp
* Notifications to Discord through webhooks

Please report issus on [github](https://github.com/ZettaIO/restic-compose-backup/issues).

Automatically detects and backs up volumes, mysql, mariadb and postgres databases in a docker-compose setup.

* Each service in the compose setup is configured with a label
  to enable backup of volumes or databases
* When backup starts a new instance of the container is created
  mapping in all the needed volumes. It will copy networks etc
  to ensure databases can be reached
* Volumes are mounted to `/volumes/<service_name>/<path>`
  in the backup process container. `/volumes` is pushed into restic
* Databases are backed up from stdin / dumps into restic using path `/databases/<service_name>/dump.sql`
* Cron triggers backup at 2AM every day

## Install

```bash
docker pull zettaio/restic-compose-backup
```

.. or clone this repo and build it.

## Configuration

Required env variables for restic:

```bash
RESTIC_REPOSITORY
RESTIC_PASSWORD
```

Backend specific env vars : https://restic.readthedocs.io/en/stable/040_backup.html#environment-variables

Additional env vars:

```bash
# Prune rules
RESTIC_KEEP_DAILY=7
RESTIC_KEEP_WEEKLY=4
RESTIC_KEEP_MONTHLY=12
RESTIC_KEEP_YEARLY=3

# Logging level (debug,info,warning,error)
LOG_LEVEL=info

# SMTP alerts
EMAIL_HOST=my.mail.host
EMAIL_PORT=465
EMAIL_HOST_USER=johndoe
EMAIL_HOST_PASSWORD=s3cr3tpassw0rd
EMAIL_SEND_TO=johndoe@gmail.com

# Discord webhook
DISCORD_WEBHOOK=https://discordapp.com/api/webhooks/...
```

### Volumes

```yaml
version: '3'
services:
  # The backup service
  backup:
    build: restic-compose-backup
    environment:
      - RESTIC_REPOSITORY=<whatever restic supports>
      - RESTIC_PASSWORD=hopefullyasecturepw
      - RESTIC_KEEP_DAILY=7
      - RESTIC_KEEP_WEEKLY=4
      - RESTIC_KEEP_MONTHLY=12
      - RESTIC_KEEP_YEARLY=3
    env_file:
      - some_other_vars.env
    volumes:
      - /var/run/docker.sock:/tmp/docker.sock:ro

  example:
    image: some_image
    # Enable volume backup with label
    labels:
      restic-compose-backup.volumes: true
    # These volumes will be backed up
    volumes:
      # Docker volume
      - media:/srv/media
      # Host map
      - /srv/files:/srv/files

volumes:
  media:
```

A simple `include` and `exclude` filter is also available.

```yaml
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

```

Exclude

```yaml
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
```

### Databases

Will dump databases directly into restic through stdin.
They will appear in restic as a separate snapshot with
path `/databases/<service_name>/dump.sql` or similar.

```yaml
  mariadb:
    image: mariadb:10
    labels:
      restic-compose-backup.mariadb: true
```

```yaml
  mysql:
    image: mysql:5
    labels:
      restic-compose-backup.mysql: true
```

```yaml
  postgres:
    image: postgres
    labels:
      restic-compose-backup.postgres: true
```


## Running Tests

```bash
python setup.py develop
pip install -r tests/requirements.txt
pytest tests
```

## Building Docs

```bash
pip install -r docs/requirements.txt
python setup.py build_sphinx
```

## Contributing

Contributions are welcome regardless of experience level. Don't hesitate submitting issues, opening partial or completed pull requests.