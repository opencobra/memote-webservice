# Memote Webservice

**N.B.: All relevant development of the web service is happening at https://github.com/DD-DeCaF/memote-webservice. Some deployment details are DD-DeCaF specific but we currently do not have the resources to maintain both. This repository is therefore archived.**

![master Branch](https://img.shields.io/badge/branch-master-blue.svg)
[![master Build Status](https://travis-ci.org/opencobra/memote-webservice.svg?branch=master)](https://travis-ci.org/opencobra/memote-webservice)
[![master Codecov](https://codecov.io/gh/opencobra/memote-webservice/branch/master/graph/badge.svg)](https://codecov.io/gh/opencobra/memote-webservice/branch/master)
[![master Requirements Status](https://requires.io/github/opencobra/memote-webservice/requirements.svg?branch=master)](https://requires.io/github/opencobra/memote-webservice/requirements/?branch=master)

![devel Branch](https://img.shields.io/badge/branch-devel-blue.svg)
[![devel Build Status](https://travis-ci.org/opencobra/memote-webservice.svg?branch=devel)](https://travis-ci.org/opencobra/memote-webservice)
[![devel Codecov](https://codecov.io/gh/opencobra/memote-webservice/branch/devel/graph/badge.svg)](https://codecov.io/gh/opencobra/memote-webservice/branch/devel)
[![devel Requirements Status](https://requires.io/github/opencobra/memote-webservice/requirements.svg?branch=devel)](https://requires.io/github/opencobra/memote-webservice/requirements/?branch=devel)

## Post-cookiecutter steps

Perform the following steps after creating a new service from the cookiecutter.

* Create the following environment variables in Travis CI:
  * `ENVIRONMENT`: `testing`
  * `FLASK_APP`: `src/memote_webservice/wsgi.py`
  * `SLACK_ACCOUNT`: Workspace name, e.g. `biosustain`
  * `SLACK_TOKEN`: [Find it here](https://biosustain.slack.com/services/B8D8VKW3W)
  * `SLACK_CHANNEL`: Normally `#decaf-notifications`
  * `DOCKER_PASSWORD`: For push access to [Docker Hub](https://hub.docker.com/u/dddecaf/dashboard/)
* Remove this section from the README.

## Development

Run `make setup` first when initializing the project for the first time. Type
`make` to see all commands.

### Environment

Specify environment variables in a `.env` file. See `docker-compose.yml` for the
possible variables and their default values.

* Set `ENVIRONMENT` to either
  * `development`,
  * `testing`, or
  * `production`.
* `SECRET_KEY` Flask secret key. Will be randomly generated in development and testing environments.
* `SENTRY_DSN` DSN for reporting exceptions to
  [Sentry](https://docs.sentry.io/clients/python/integrations/flask/).
* `ALLOWED_ORIGINS`: Comma-seperated list of CORS allowed origins.
