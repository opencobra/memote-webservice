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

"""Provide a resource to submit models for testing."""

from bz2 import BZ2File
from gzip import GzipFile
from io import BytesIO
from itertools import chain

import redis
import structlog
from cobra.io import load_json_model, read_sbml_model, load_yaml_model
from cobra.io.sbml3 import CobraSBMLError
from flask_restplus import Resource
from rq import Queue, Connection
from werkzeug.datastructures import FileStorage

from memote_webservice.app import app, api

__all__ = ("Submit",)

LOGGER = structlog.get_logger(__name__)


@api.route("/submit")
class Submit(Resource):
    """Submit a metabolic model for testing."""

    JSON_TYPES = {
        "application/json",
        "text/json"
    }
    XML_TYPES = {
        "application/xml",
        "text/xml"
    }
    upload_parser = api.parser()
    upload_parser.add_argument(
        "model", location="files", type=FileStorage, required=True,
        nullable=False, help="No model file was submitted in field 'model'.")

    @api.doc(parser=upload_parser, responses={
                 202: "Success",
                 400: "Bad Request",
                 415: "Bad media type"
    })
    def post(self):
        """Load a metabolic model and submit it for testing by memote."""
        upload = self.upload_parser.parse_args(strict=True)["model"]
        model = self._load_model(upload)
        job_id = self._submit(model)
        return {"uuid": job_id}, 202

    def _submit(self, model):
        LOGGER.debug("Create connection to '%s'.", app.config["REDIS_URL"])
        with Connection(redis.from_url(app.config["REDIS_URL"])):
            LOGGER.debug("Using queue '%s'.", app.config["QUEUES"][0])
            queue = Queue(app.config["QUEUES"][0],
                          default_timeout=app.config["QUEUE_TIMEOUT"][0])
            job = queue.enqueue(
                "jobs.model_snapshot", args=(model,),
                ttl=app.config["JOB_TTL"][0],
                result_ttl=app.config["RESULT_TTL"][0])
            LOGGER.debug(f"Successfully submitted job '{job.get_id()}'.")
        return job.get_id()

    def _load_model(self, file_storage):
        try:
            filename, content = self._decompress(file_storage.filename.lower(),
                                                 file_storage)
        except IOError as err:
            msg = "Failed to decompress file."
            LOGGER.exception(msg)
            api.abort(400, msg, error=str(err))
        try:
            if file_storage.mimetype in self.JSON_TYPES or \
                    filename.endswith("json"):
                LOGGER.debug("Loading model from JSON.")
                model = load_json_model(content)
            elif file_storage.mimetype in self.XML_TYPES or \
                    filename.endswith("xml") or filename.endswith("sbml"):
                LOGGER.debug("Loading model from SBML.")
                model = read_sbml_model(content)
            else:
                msg = f"'{file_storage.mimetype}' is an unhandled MIME type."
                LOGGER.error(msg)
                api.abort(415, msg, recognizedMIMETypes=list(chain(
                    self.JSON_TYPES, self.XML_TYPES)))
        except (CobraSBMLError, ValueError) as err:
            msg = "Failed to parse model."
            LOGGER.exception(msg)
            api.abort(400, msg, error=str(err))
        finally:
            content.close()
            file_storage.close()
        return model

    @staticmethod
    def _decompress(filename, content):
        if filename.endswith(".gz"):
            filename = filename[:-3]
            LOGGER.debug("Unpacking gzip compressed file.")
            with GzipFile(fileobj=content, mode="rb") as zipped:
                content = BytesIO(zipped.read())
        elif filename.endswith(".bz2"):
            filename = filename[:-4]
            LOGGER.debug("Unpacking bzip2 compressed file.")
            with BZ2File(content, mode="rb") as zipped:
                content = BytesIO(zipped.read())
        else:
            content = BytesIO(content.read())
        return filename, content
