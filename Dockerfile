FROM restic/restic

ADD requirements.txt /
RUN apk update && apk add python3 dcron
RUN pip3 install -r requirements.txt

ADD restic-backup /restic-backup

WORKDIR /restic-backup

ENTRYPOINT []
CMD ["/restic-backup/entrypoint.sh"]
