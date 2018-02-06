"""
Support for TiVo TCP Remote Protocol.

For the protocol documentation see
https://lv.tivo.com/assets/images/abouttivo/resources/downloads/brochures/TiVo_TCP_Network_Remote_Control_Protocol.pdf

Somee possible non-documented commands include:
 IRCODE NETFLIX : switch to the netflix app if available.
 IRCODE FIND_REMOTE : if the remote supports this, makes a noise.

More details for stored recordings:
https://IPADDRESS/TiVoConnect?Command=QueryContainer&Container=%2FNowPlaying&Recurse=Yes
Note this will need the device Media Access Code as a http password.
"""

import socket
import logging

# To see the logs:
# logger = logging.getLogger()
# logger.setLevel(logging.DEBUG)

SCREEN_LIVETV = 'LIVETV'
SCREEN_TIVO = 'TIVO'
SCREEN_NOWPLAYING = 'NOWPLAYING'
SCREEN_GUIDE = 'GUIDE'

VALID_SCREENS = (SCREEN_LIVETV, SCREEN_TIVO, SCREEN_GUIDE, SCREEN_NOWPLAYING)

class MissingHostParameter(Exception):
    pass

class Remote():
    """TiVo Remote Protocol handler."""

    def __init__(self, config):
        """Initialize the object with a configuration dictionary.
        The config must contain a host.
        Port defaults to 31339 if not set.
        The timeout defaults to 100ms."""
        if not 'host' in config:
            raise MissingHostParameter()
        if not 'port' in config:
            config['port'] = 31339
        if not 'timeout' in config:
            config['timeout'] = 0.250
        self._config = config
        self._status = None
        self._screen = SCREEN_LIVETV
        self._connection = None

    def __enter__(self):
        return self.connect()

    def __exit__(self, type, value, traceback):
        self.close()

    def connect(self):
        """Open a connection to the configured device and store the status response."""
        self._connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        if 'timeout' in self._config and self._config['timeout']:
            self._connection.settimeout(self._config['timeout'])
        self._connection.connect((self._config['host'], self._config['port']))
        self._status = self._read_response(True)
        return self._connection

    def close(self):
        """Close any existing network connection."""
        if self._connection:
            self._connection.close()
            self._connection = None

    def send_keyboard(self, key):
        """Send a keyboard code to the device.

        If the code yields a status response, extracts and updates the channel information.
        See the protocol documentation for details of valid codes."""
        with self.connect() as connection:
            msg = "KEYBOARD {0}\r".format(key).encode('ASCII')
            connection.send(msg)
            r = self._read_response()
            r = self._read_response().split(' ')
            if r[0] == 'CH_STATUS':
                self._channel = r[1]
            logging.debug(r)

    def send_ircode(self, code):
        """Send an IRCODE to the device."""
        with self.connect() as connection:
            msg = "IRCODE {0}\r".format(code).encode('ASCII')
            connection.send(msg)
            r = self._read_response().split(' ')
            if r[0] == 'CH_STATUS':
                self._channel = r[1]
            logging.debug(r)

    def set_channel(self, channel):
        """Set the channel and update the channel state."""
        with self.connect() as connection:
            msg = "SETCH {0}\r".format(channel).encode('ASCII')
            connection.send(msg)
            r = self._read_response().split(' ')
            if r[0] == 'CH_STATUS':
                self._channel = r[1]
            logging.debug(r)

    def teleport(self, screen):
        """Navigate to one of several defined screens.

           TIVO: the main menu screen
           LIVETV: live TV viewing
           GUIDE: the program guide screen
           NOWPLAYING: list of recordings
        """
        with self.connect() as connection:
            msg = "TELEPORT {0}\r".format(screen).encode('ASCII')
            connection.send(msg)
            r = self._read_response()
            logging.debug(r)
            if r == 'LIVETV_READY':
                self._screen = SCREEN_LIVETV
            elif screen in VALID_SCREENS:
                index = VALID_SCREENS.index(screen)
                self._screen = VALID_SCREENS[index]
            else:
                self._screen = SCREEN_LIVETV

    def _read_response(self, first_time=False):
        """Read any response from the device and convert back to text.
        Returns an empty string if no response was provided."""
        try:
            data = self._connection.recv(1024)
            msg = data.decode('ASCII').rstrip()
        except socket.timeout:
            msg = ''
        return msg

    @property
    def channel(self):
        """Get the current channel number."""
        with self.connect() as conn:
            r = self._status.split(' ')
            if r[0] == 'CH_STATUS':
                self._channel = r[1]
        return self._channel

    @property
    def screen(self):
        """Get the current DVR screen.

        As the remote protocol cannot query for the current screen,
        it defaults to SCREEN_LIVETV."""
        return self._screen
