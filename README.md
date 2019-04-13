
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
  some_service:
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