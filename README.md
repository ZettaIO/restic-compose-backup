
# restic-volume-backup

*WORK IN PROGRESS*

Backup using using https://restic.net/ for a docker-compose setup.

Automatically detects and backs up volumes in a docker-compose setup.
This includes both host mapped volumes and actual docker volumes.

* Cron triggers backup
* Volumes for all running containers are backed up

## Configuration

```bash
RESTIC_REPOSITORY
RESTIC_PASSWORD
```
