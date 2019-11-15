FROM restic/restic:0.9.5

RUN apk update && apk add python3 dcron mariadb-client postgresql-client

ADD . /restic-volume-backup
WORKDIR /restic-volume-backup
RUN pip3 install -U pip setuptools
RUN python3 setup.py develop && pip3 install .

ENTRYPOINT []
CMD ["./entrypoint.sh"]
