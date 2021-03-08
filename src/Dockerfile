FROM alpine AS builder

RUN mkdir -p /opt

ARG IMAGE_ARCH=amd64

ARG RCON_CLI_VERSION=1.4.4

ADD https://github.com/itzg/rcon-cli/releases/download/${RCON_CLI_VERSION}/rcon-cli_${RCON_CLI_VERSION}_linux_${IMAGE_ARCH}.tar.gz /tmp/rcon-cli.tar.gz

RUN tar x -f /tmp/rcon-cli.tar.gz -C /opt/ && \
    chmod +x /opt/rcon-cli

RUN apk -U --no-cache add \
    build-base \
    build-dependencies \
    gcc \
    wget \
    git \
    curl \
    openssl-dev \
    mariadb-dev \
    makec

ADD mydumper /usr/src/
WORKDIR /usr/src

RUN \
  cmake . && \
  make && \
  make install

FROM restic/restic

RUN apk -U --no-cache add \
    bash \
    coreutils \
    openssh-client \
    python3 py3-pip \
    dcron \
    mariadb-client \
    postgresql-client

COPY --from=builder /opt/rcon-cli /opt/rcon-cli
COPY --from=builder /usr/bin/mydumper /usr/bin/mydumper

RUN ln -s /opt/rcon-cli /usr/bin

# install rcb python app

ADD . /restic-compose-backup
WORKDIR /restic-compose-backup

RUN pip3 install -U pip setuptools wheel && pip3 install -e .
ENV XDG_CACHE_HOME=/cache

# end install

ENTRYPOINT []
CMD ["./entrypoint.sh"]
