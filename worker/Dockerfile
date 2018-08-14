FROM python:3.6-slim

ENV PYTHONUNBUFFERED=1

ENV APP_USER=kaa
ENV HOME="/home/${APP_USER}"

ARG UID=1000
ARG GID=1000

ARG CWD="${HOME}/app"

ENV PYTHONPATH="${CWD}/src"

RUN groupadd --system --gid "${GID}" "${APP_USER}" \
    && useradd --system --create-home --home-dir "${HOME}" \
        --uid "${UID}" --gid "${APP_USER}" "${APP_USER}"

WORKDIR "${CWD}"

COPY Pipfile* "${CWD}/"

# `g++` is required for building `gevent` but all build dependencies are
# later removed again.
RUN set -eux \
    && ln -sf /usr/local/bin/python /bin/python \
    && apt-get update \
    && apt-get install --yes --only-upgrade openssl ca-certificates \
    && pip install --upgrade pip==9.0.3 setuptools wheel pipenv==11.10.0 \
    && pipenv install --system --dev --deploy \
    && rm -rf /root/.cache/pip \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*

COPY . "${CWD}/"

RUN chown -R "${APP_USER}:${APP_USER}" "${CWD}"
