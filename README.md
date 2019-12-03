
# restic-compose-backup

*WORK IN PROGRESS*

Backup using https://restic.net/ for a docker-compose setup.

Automatically detects and backs up volumes, mysql, mariadb and postgres databases in a docker-compose setup.
This includes both host mapped volumes and actual docker volumes.

* Each service in the compose setup is configured with a label
  to enable backup of volumes or databases
* When backup starts a new instance of the container is created
  mapping in all the needed volumes. It will copy networks etc
  to ensure databases can be reached
* Volumes are mounter to `/backup/<service_name>/<path>`
  in the backup process container. `/backup` is pushed into restic
* Databases are backed up from stdin / dumps
* Cron triggers backup

## Configuration

Required env variables for restic:

```bash
RESTIC_REPOSITORY
RESTIC_PASSWORD
```

Backend specific env vars : https://restic.readthedocs.io/en/stable/040_backup.html#environment-variables

### Volumes

```yaml
version: '3'
services:
  # The backup service
  backup:
    build: restic-volume-backup
    environment:
      - RESTIC_REPOSITORY=<whatever restic supports>
      - RESTIC_PASSWORD=hopefullyasecturepw
    env_file:
      - some_other_vars.env
    volumes:
      - /var/run/docker.sock:/tmp/docker.sock:ro

  example:
    image: some_image
    # Enable volume backup with label
    labels:
      restic-volume-backup.enabled: true
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
      restic-volume-backup.volumes: true
      restic-volume-backup.volumes.include: "files,data"
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
      restic-volume-backup.volumes: true
      restic-volume-backup.volumes.exclude: "media"
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
path `/backup/<service_name>/dump.sql` or similar.

```yaml
  mariadb:
    image: mariadb:10
    labels:
      restic-volume-backup.mariadb: true
```

```yaml
  mysql:
    image: mysql:5
    labels:
      restic-volume-backup.mysql: true
```

```yaml
  postgres:
    image: postgres
    labels:
      restic-volume-backup.postgres: true
```


## Running Tests

```
python setup.py develop
pip install -r tests/requirements.txt
pytest tests
```
