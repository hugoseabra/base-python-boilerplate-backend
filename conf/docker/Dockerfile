# -----------------------------------------------------------------------------
# Docker IMAGE wiseloan/core
# docker build --rm -t core .
# docker tag catalog <repo_url>/wiseloan-core:<tag>
# -----------------------------------------------------------------------------
FROM --platform=linux/amd64 python:3.10-slim-buster as base

# Celery does not work with root unless you force it
ENV C_FORCE_ROOT true

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

LABEL app.boilerplate.image.name="boilerplate-base"

# Install packages needed to run your application (not build deps):
# We need to recreate the /usr/share/man/man{1..8} directories first because
# they were clobbered by a parent image.
RUN set -ex \
    && RUN_DEPS=" \
        apt-utils \
        build-essential \
        nano \
        curl \
        libpcre3 \
        libtiff5-dev \
        zlib1g-dev \
        libpcre3 \
        libpcre3-dev \
        libjpeg62 \
        libjpeg62-turbo-dev \
        libfreetype6-dev \
        libwebp-dev \
        liblcms2-dev \
        libxml2-dev \
        libxslt-dev \
        python-dev \
        postgresql-client \
    " \
    && seq 1 8 | xargs -I{} mkdir -p /usr/share/man/man{} \
    && apt-get update && apt-get install -y --no-install-recommends $RUN_DEPS \
    && apt-mark hold python2 python2-minimal python2.7 python2.7-minimal libpython2-stdlib libpython2.7-minimal libpython2.7-stdlib \
    && apt-get purge -y --auto-remove -o APT::AutoRemove::RecommendsImportant=false $BUILD_DEPS \
    && apt-get clean && rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*

# -----------------------------------------------------------------------------
FROM base AS builder

RUN set -ex \
    && pip3 install -I -U pip setuptools poetry==1.3.1

WORKDIR /code/app

COPY ./pyproject.toml /code/.
COPY ./poetry.lock /code/.
COPY ./conf/docker /code/conf

# Install build deps
RUN set -ex \
    && cd /code \
    && poetry config virtualenvs.create false \
    && poetry config installer.max-workers 10 \
    && poetry install --without dev --no-root --no-interaction --no-ansi \
    && rm -rf /root/.cache/pip/*

# direct python server will listen to this port
EXPOSE 8000

# -----------------------------------------------------------------------------
FROM builder AS development

LABEL app.boilerplate.image.name="boilerplate-dev"

RUN set -ex \
    && RUN_DEPS=" \
        graphviz \
        graphviz-dev \
    " \
    && seq 1 8 | xargs -I{} mkdir -p /usr/share/man/man{} \
    && apt-get update && apt-get install -y --no-install-recommends $RUN_DEPS \
    && apt-get purge -y --auto-remove -o APT::AutoRemove::RecommendsImportant=false $BUILD_DEPS \
    && apt-get clean && rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*

RUN set -ex \
    && poetry install --no-root --no-interaction --no-ansi \
    && rm -rf /root/.cache/pip/*

# -----------------------------------------------------------------------------
FROM builder AS release

RUN set -ex \
    && pip3 install -U gunicorn==20.1.0 \
    && rm -rf /root/.cache/pip/*

ENV DEBUG=false

ARG USERNAME=docker
ARG UID=123
ARG GID=4567

RUN addgroup --gid ${GID} ${USERNAME}
RUN useradd -ms /bin/bash ${UID} --uid ${UID} --home /home/${USERNAME}
RUN usermod -a -G ${GID} ${UID}
RUN chown -R ${UID}:${GID} /code

USER ${UID}

COPY . .

CMD ["/code/conf/services/gunicorn.sh"]

# -----------------------------------------------------------------------------
FROM release AS staging

LABEL app.boilerplate.image.name="boilerplate-staging"

# -----------------------------------------------------------------------------
FROM release AS production

LABEL app.boilerplate.image.name="boilerplate-production"