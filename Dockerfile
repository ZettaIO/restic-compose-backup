FROM restic/restic

RUN apk update && apk add python3 dcron mariadb-client postgresql-client

ADD . /restic-volume-backup
WORKDIR /restic-volume-backup
RUN pip3 install -U pip setuptools && python3 setup.py develop

ENTRYPOINT []
CMD ["/restic-backup/entrypoint.sh"]
