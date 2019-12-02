FROM restic/restic:0.9.6

RUN apk update && apk add python3 dcron mariadb-client postgresql-client

ADD . /restic-volume-backup
WORKDIR /restic-volume-backup
RUN pip3 install -U pip setuptools
RUN pip3 install -e .

ENTRYPOINT []
CMD ["./entrypoint.sh"]
