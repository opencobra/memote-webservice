# memote Webservice

![master Branch](https://img.shields.io/badge/branch-master-blue.svg)
[![master Build Status](https://travis-ci.org/DD-DeCaF/memote-webservice.svg?branch=master)](https://travis-ci.org/DD-DeCaF/memote-webservice)
[![master Codecov](https://codecov.io/gh/DD-DeCaF/memote-webservice/branch/master/graph/badge.svg)](https://codecov.io/gh/DD-DeCaF/memote-webservice/branch/master)
[![master Requirements Status](https://requires.io/github/DD-DeCaF/memote-webservice/requirements.svg?branch=master)](https://requires.io/github/DD-DeCaF/memote-webservice/requirements/?branch=master)

![devel Branch](https://img.shields.io/badge/branch-devel-blue.svg)
[![devel Build Status](https://travis-ci.org/DD-DeCaF/memote-webservice.svg?branch=devel)](https://travis-ci.org/DD-DeCaF/memote-webservice)
[![devel Codecov](https://codecov.io/gh/DD-DeCaF/memote-webservice/branch/devel/graph/badge.svg)](https://codecov.io/gh/DD-DeCaF/memote-webservice/branch/devel)
[![devel Requirements Status](https://requires.io/github/DD-DeCaF/memote-webservice/requirements.svg?branch=devel)](https://requires.io/github/DD-DeCaF/memote-webservice/requirements/?branch=devel)

## Post-cookiecutter steps

Perform the following steps after creating a new service from the cookiecutter.

* Create kubernetes secrets `memote-webservice-production` and `memote-webservice-staging`. Values needed:
  * `SECRET_KEY` (see [How to generate good secret keys](http://flask.pocoo.org/docs/1.0/quickstart/#sessions))
  * `SENTRY_DSN`
* Review the cpu/memory limits in `deployment/deployment.yml` under `resources` ([see documentation](https://kubernetes.io/docs/concepts/configuration/manage-compute-resources-container/))
* Create the following environment variables in Travis CI:
  * `ENVIRONMENT`: `testing`
  * `GCLOUD_EMAIL`: Google Cloud service account email for Travis CI
  * `GCLOUD_KEY`: Google Cloud service account key for Travis CI (JSON file base64-encoded)
* Generate secure token for Slack notifications in `.travis.yml`
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
