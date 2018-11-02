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

"""Define workers that chow through the queue."""

import os
import sys

import jobs  # Pre-load job functions and libraries for performance.
import redis
from rq import Connection, Worker


with Connection(redis.from_url(os.environ["REDIS_URL"])):
    worker = Worker(sys.argv[1:] or ["default"])
    worker.work()
