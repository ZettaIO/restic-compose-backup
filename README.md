
# restic-volume-backup

*WORK IN PROGRESS*

Backup using using https://restic.net/ for a docker-compose setup.

Automatically detects and backs up volumes in a docker-compose setup.
This includes both host mapped volumes and actual docker volumes.

* Cron triggers backup
* Volumes for all running containers are backed up

## Configuration

Required env variables for restic:

```bash
RESTIC_REPOSITORY
RESTIC_PASSWORD
```

Example compose setup:

```yaml
version: '3'
services:
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

Include

```yaml
example:
    image: some_image
    labels:
      restic-volume-backup.enabled: true
      restic-volume-backup.include: "files,data"
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

Exclude:

```yaml
example:
    image: some_image
    labels:
      restic-volume-backup.enabled: true
      restic-volume-backup.exclude: "media"
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
