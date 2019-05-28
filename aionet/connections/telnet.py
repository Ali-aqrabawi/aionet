"""
Telnet Connection Module
"""
import asyncio
from aionet.exceptions import DisconnectError, TimeoutError
from aionet.connections.base import BaseConnection


class TelnetConnection(BaseConnection):
    def __init__(self,
                 host=u"",
                 username=u"",
                 password=u"",
                 port=23,
                 timeout=15,
                 loop=None,
                 pattern=None, ):
        super().__init__()
        if host:
            self._host = host
        else:
            raise ValueError("Host must be set")
        self._port = int(port)
        self._timeout = timeout
        self._username = username
        self._password = password
        if loop is None:
            self._loop = asyncio.get_event_loop()
        else:
            self._loop = loop

        if pattern is not None:
            self._pattern = pattern

        self._timeout = timeout

    async def _start_session(self):
        """ start Telnet Session by login to device """
        self._logger.info("Host {}: telnet: trying to login to device".format(self._host))
        output = await self.read_until_pattern(['username', 'Username'])
        self.send(self._username + '\n')
        output += await self.read_until_pattern(['password', 'Password'])
        self.send(self._password + '\n')
        output += await self.read_until_prompt()
        self.send('\n')
        if 'Login invalid' in output:
            raise DisconnectError(self._host, None, "authentication failed")

    def __check_session(self):
        if not self._stdin:
            raise RuntimeError("telnet session not started")

    @asyncio.coroutine
    def connect(self):
        """ Establish Telnet Connection """
        self._logger.info("Host {}: telnet: Establishing Telnet Connection on port {}".format(self._host, self._port))
        fut = asyncio.open_connection(self._host, self._port, family=0, flags=0)
        try:
            self._stdout, self._stdin = yield from asyncio.wait_for(fut, self._timeout)
        except asyncio.TimeoutError:
            raise TimeoutError(self._host)
        except Exception as e:
            raise DisconnectError(self._host, None, str(e))

        yield from self._start_session()

    async def disconnect(self):
        """ Gracefully close the Telnet connection """
        self._logger.info("Host {}: telnet: Disconnecting".format(self._host))
        self._logger.info("Host {}: telnet: Disconnecting".format(self._host))
        self._conn.close()
        await self._conn.wait_closed()

    def send(self, cmd):
        self._stdin.write(cmd.encode())

    async def read(self):
        output = await self._stdout.read(self._MAX_BUFFER)
        return output.decode(errors='ignore')

    async def close(self):
        pass
