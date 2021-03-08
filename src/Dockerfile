FROM alpine AS builder

RUN mkdir -p /opt

ARG IMAGE_ARCH=amd64

ARG RCON_CLI_VERSION=1.4.4

ADD https://github.com/itzg/rcon-cli/releases/download/${RCON_CLI_VERSION}/rcon-cli_${RCON_CLI_VERSION}_linux_${IMAGE_ARCH}.tar.gz /tmp/rcon-cli.tar.gz

RUN tar x -f /tmp/rcon-cli.tar.gz -C /opt/ && \
    chmod +x /opt/rcon-cli

FROM restic/restic

RUN apk -U --no-cache add \
    bash \
    coreutils \
    openssh-client \
    python3 py3-pip \
    dcron \
    mariadb-client \
    postgresql-client

RUN apk -U --no-cache add \
    build-base \
    gcc \
    wget \
    git \
    curl \
    openssl-dev \
    mariadb-dev \
    cmake \
    glib-dev \
    zlib-dev \
    pcre-dev

ADD mydumper /usr/src/
WORKDIR /usr/src

RUN cmake -DWITH_SSL=OFF . && \
   make && \
   make install

COPY --from=builder /opt/rcon-cli /opt/rcon-cli

RUN ln -s /opt/rcon-cli /usr/bin

# install rcb python app

ADD . /restic-compose-backup
WORKDIR /restic-compose-backup

RUN pip install -U pip setuptools wheel && pip install -e .
ENV XDG_CACHE_HOME=/cache

# end install

ENTRYPOINT []
CMD ["./entrypoint.sh"]
