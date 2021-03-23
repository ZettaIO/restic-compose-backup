#!/bin/sh

# Dump all env vars so we can source them in cron jobs
printenv | sed 's/^\(.*\)$/export \1/g' > /env.sh

# Update CA certificates
update-ca-certificates

# Write crontab
rcb crontab > crontab

# start cron in the foreground
crontab crontab
crond -f
