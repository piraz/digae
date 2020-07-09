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

from . import services
from firenado import service, tornadoweb


class IndexHandler(tornadoweb.TornadoHandler):

    def get(self):
        self.write("HELLO")


class LoginHandler(tornadoweb.TornadoHandler):

    @service.served_by(services.SMTPService, "smtp_service")
    async def get(self):
        server = await self.smtp_service.get_server("ipe.projenv.net", port=25)
        await self.smtp_service.login(
            server, "flavio.garcia@viamaple.com", "pir@tone$"
        )
        await self.smtp_service.quit(server)
