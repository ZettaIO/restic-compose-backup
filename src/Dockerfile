FROM restic/restic:0.9.6

RUN apk update && apk add python3 dcron mariadb-client postgresql-client

ADD . /restic-compose-backup
WORKDIR /restic-compose-backup
RUN pip3 install -U pip setuptools wheel && pip3 install -e .
ENV XDG_CACHE_HOME=/cache

ENTRYPOINT []
CMD ["./entrypoint.sh"]
