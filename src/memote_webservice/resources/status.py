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

import redis
import structlog
from flask import abort
from flask_restplus import Resource
from rq import Connection, Queue

from memote_webservice.app import api, app


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
        """Return queue information about a job."""
        LOGGER.debug("Create connection to '%s'.", app.config["REDIS_URL"])
        with Connection(redis.from_url(app.config["REDIS_URL"])):
            LOGGER.debug("Using queue '%s'.", app.config["QUEUES"][0])
            queue = Queue(app.config["QUEUES"][0])
            job = queue.fetch_job(uuid)
        if job is None:
            msg = f"Result {uuid} does not exist."
            LOGGER.error(msg)
            abort(404, msg)
        return {
            "finished": job.is_finished,
            "status": job.get_status()
        }
