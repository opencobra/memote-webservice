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

import structlog
from cobra.io import load_json_model, read_sbml_model
from cobra.io.sbml3 import CobraSBMLError
from flask import abort
from flask_apispec import MethodResource, doc, marshal_with, use_kwargs

from memote_webservice.schemas import SubmitRequest, SubmitResponse
from memote_webservice.tasks import model_snapshot


__all__ = ("Submit",)

LOGGER = structlog.get_logger(__name__)


class Submit(MethodResource):
    """Submit a metabolic model for testing."""

    JSON_TYPES = {
        "application/json",
        "text/json"
    }
    XML_TYPES = {
        "application/xml",
        "text/xml"
    }

    @doc(description="Load a metabolic model and submit it for testing by "
                     "memote.")
    @use_kwargs(SubmitRequest, locations=('files',))
    @marshal_with(SubmitResponse, code=202)
    @marshal_with(None, code=400)
    @marshal_with(None, code=415)
    def post(self, model):
        try:
            model = self._load_model(model)
            job_id = self._submit(model)
            return {"uuid": job_id}, 202
        except Exception as e:
            abort(400, f"{type(e).__name__}: {str(e)}")

    def _submit(self, model):
        result = model_snapshot.delay(model)
        LOGGER.debug(f"Successfully submitted job '{result.id}'.")
        return result.id

    def _load_model(self, file_storage):
        try:
            filename, content = self._decompress(file_storage.filename.lower(),
                                                 file_storage)
        except IOError as err:
            msg = f"Failed to decompress file: {str(err)}"
            LOGGER.exception(msg)
            abort(400, msg)
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
                mime_types = ', '.join((chain(self.JSON_TYPES, self.XML_TYPES)))
                msg = (
                    f"'{file_storage.mimetype}' is an unhandled MIME type. "
                    f"Recognized MIME types are: {mime_types}"
                )
                LOGGER.warning(msg)
                abort(415, msg)
        except (CobraSBMLError, ValueError) as err:
            msg = f"Failed to parse model: {str(err)}"
            LOGGER.exception(msg)
            abort(400, msg)
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
