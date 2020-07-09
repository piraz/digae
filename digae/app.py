#!/usr/bin/env python
#
# Copyright 2020 Flavio Garcia
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

from . import handlers
from firenado import tornadoweb
# See: https://bit.ly/3dWd8QJ
from concurrent.futures import ThreadPoolExecutor

MAX_WORKERS = 5


class DigaeComponent(tornadoweb.TornadoComponent):

    def __init__(self, name, application):
        super(DigaeComponent, self).__init__(name, application)
        self._executor = ThreadPoolExecutor(max_workers=MAX_WORKERS)

    @property
    def executor(self):
        return self._executor

    def shutdown(self):
        self._executor.shutdown(wait=False)

    def get_handlers(self):
        return [
            (r'/', handlers.IndexHandler),
            (r'/login', handlers.LoginHandler),
        ]
