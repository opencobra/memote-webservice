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

"""Test expected functioning of the OpenAPI docs endpoints."""

import os
from urllib.parse import urljoin


def test_swagger_docs(client):
    """Expect the OpenAPI docs to be served as HTML."""
    endpoint = urljoin(os.environ["SCRIPT_NAME"], "/")
    resp = client.get(endpoint)
    assert resp.status_code == 200
    assert resp.content_type == "text/html; charset=utf-8"


def test_swagger_json(client):
    """Expect the OpenAPI docs to be served as JSON."""
    endpoint = urljoin(os.environ["SCRIPT_NAME"], "/swagger.json")
    resp = client.get(endpoint)
    assert resp.status_code == 200
    assert resp.content_type == "application/json"
