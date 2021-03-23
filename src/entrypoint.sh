#!/bin/sh

set -e

setup_cacerts(){

  update-ca-certificates
}

dump_env(){

  # Dump all env vars so we can source them in cron jobs
  printenv | sed 's/^\(.*\)$/export \1/g' > /env.sh
}

setup_crontab(){

  # Write crontab
  rcb crontab > crontab

  # start cron in the foreground
  crontab crontab
  crond -f
}

start_app(){
  
  setup_cacerts

  if [ "$1" = '' ]; then
    dump_env
    setup_crontab
  else
    exec "$@"
  fi
}

start_app "$@"
