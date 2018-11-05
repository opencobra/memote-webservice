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
from flask_restplus import Resource

from memote_webservice.app import api
from memote_webservice.celery import celery_app


__all__ = ("Status",)

LOGGER = structlog.get_logger(__name__)


@api.route("/status/<string:uuid>")
@api.doc(params={"uuid": "A unique result identifier."}, responses={
    200: "Success",
    404: "Result not found"
})
class Status(Resource):
    """Query the queue for a particular result status."""

    def get(self, uuid):
        """Return queue information about a task."""
        result = AsyncResult(id=uuid, app=celery_app)
        return {
            "finished": result.ready(),
            "status": result.state,
        }
