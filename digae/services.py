from firenado import service
import logging
from smtplib import SMTP, SMTPAuthenticationError
from socket import gaierror
from tornado.concurrent import run_on_executor

logger = logging.getLogger(__name__)


class SMTPService(service.FirenadoService):

    @property
    def executor(self):
        return self.consumer.component.executor

    @run_on_executor
    def get_server(self, address, port=587):
        """

        :param str address: Server address
        :param int port: Server port, default is 587
        :return SMTP: A connected smtp server
        """
        try:
            server = SMTP(address, port=port, timeout=10)
            server.noop()
            server.starttls()
            return server
        except gaierror as ex:
            logger.error("SMTP server address %s invalid. Error: %s" % (
                address, ex
            ))
        return None

    @run_on_executor
    def login(self, server, user, password):
        """

        :param SMTP server:
        :param str user:
        :param str password:
        :return: boolean
        """
        try:
            server.login(user, password)
            return True
        except SMTPAuthenticationError as ex:
            logger.error(
                "Failed to connect to %s with user %s using password %s. "
                "Response from server: %s." % (server.sock.server_hostname,
                                               user, len(password) * "*", ex
                                               )
            )
        return False

    @run_on_executor
    def quit(self, server):
        """

        :param SMTP server:
        """
        server.quit()
