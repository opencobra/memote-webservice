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

from celery.result import AsyncResult
import structlog
from flask import make_response
from flask_restplus import Resource

from memote_webservice.app import api, app
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


@api.route("/report/<string:uuid>")
@api.doc(params={"uuid": "A unique result identifier."}, responses={
    200: "Success",
    400: "Bad request",
})
class Report(Resource):
    """Provide endpoints for metabolic model testing."""

    representations = {
        "application/json": output_json,
        "text/html": output_html
    }

    def get(self, uuid):
        """Return a snapshot report as JSON or HTML based on Accept headers."""
        result = AsyncResult(id=uuid, app=celery_app)
        if result.ready():
            # Extract the SnapshotReport object's result attribute.
            report = result.get()
        else:
            msg = f"Result {uuid} is not yet finished."
            LOGGER.info(msg)
            api.abort(400, msg)
        return report
