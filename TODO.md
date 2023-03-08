
# TODO for 1.0

Upgrade restic to 15.x

* Make backup types generic with some standard protocol
  - New backup types can be registered
  - When a backup is started we invoke methods in the specific backend
  - The backend should have access to all information about containers
  - The backend should be able to run the command in its own container or the target container
* Don't fetch all containers for all commands. Some commands are just alerts and restic only related
* More detailed cron setup separating backup time, purge time etc
* Support mariadb
* Support influxdb
* Support backup priority (restic-compose-backup.before-backup.priority=1)
* Look at bug fixes in forks
* Use shorter label names. `rcb.priority` instead of `restic-compose-backup.before-backup.priority`
* Support simple commands in labels


## Other misc

* restic unlock needed in some cases?
* Each snapshot in restic could be tagged with the service name


* Is there some elegant way to support a restore?
* Possibly back up volumes in different snapshots?


Use generators in some way to chain actions?
Action -> Some command
Use global logger


## Dockerfile

Testing

    docker run -it --entrypoint sh --rm restic/restic:0.15.1

Will install python 3.10

    apk add --no-cache python3 py3-pip dcron

## Changelog

* Upgrade restic to 0.15.1
* Upgraded to python docker 6.0.x

## Misc

* Run rcb command
* (Optional) Collect docker info
* (Optional) Issue restic command
