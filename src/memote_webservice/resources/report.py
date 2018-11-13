# Copyright (c) 2018, Novo Nordisk Foundation Center for Biosustainability,
# Technical University of Denmark.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""Provide a resource for retrieving test results."""

import structlog
from celery.result import AsyncResult
from flask import abort, jsonify, make_response
from flask_apispec import MethodResource, doc, marshal_with

from memote_webservice.celery import celery_app


__all__ = ("Report",)

LOGGER = structlog.get_logger(__name__)


def output_json(report, code, headers=None):
    """Convert a memote report to JSON."""
    LOGGER.debug("Converting to JSON.")
    resp = make_response(report.render_json(), code)
    if headers is not None:
        resp.headers.extend(headers)
    return resp


def output_html(report, code, headers=None):
    """Convert a memote report to HTML."""
    LOGGER.debug("Converting to HTML.")
    resp = make_response(report.render_html(), code)
    if headers is not None:
        resp.headers.extend(headers)
    return resp


class Report(MethodResource):
    """Provide endpoints for metabolic model testing."""

    representations = {
        "application/json": output_json,
        "text/html": output_html
    }

    @doc(description="Return a snapshot report as JSON or HTML based on Accept "
                     "headers.")
    @marshal_with(None, code=200)
    @marshal_with(None, code=400)
    def get(self, uuid):
        result = AsyncResult(id=uuid, app=celery_app)
        if not result.ready():
            msg = f"Result {uuid} is not yet finished."
            LOGGER.info(msg)
            abort(400, msg)
        elif result.failed():
            exception = result.get(propagate=False)
            return jsonify({
                'status': result.state,
                'exception': type(exception).__name__,
                'message': str(exception),
            })
        else:
            return result.get()
