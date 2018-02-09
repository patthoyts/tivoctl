"""Command-line utility to remote control a TiVo device."""

import argparse
import logging
import socket

from . import __doc__ as doc
from . import __title__ as title
from . import __version__ as version
from . import Remote


def get_log_level(args):
    """Calculate a suitabl log level from the verbosity arguments."""
    if args.quiet:
        log_level = logging.ERROR
    elif not args.verbose:
        log_level = logging.WARNING
    elif args.verbose == 1:
        log_level = logging.INFO
    else:
        log_level = logging.DEBUG
    return log_level


def main():
    """Implement command-line tivoctl interface to the package"""

    parser = argparse.ArgumentParser(prog=title, description=doc,
                                     epilog="e.g. %(prog)s --host 192.168.0.10 --ircode CHANNELUP")
    parser.add_argument("--version", action="version",
                        version="%(prog)s {0}".format(version))
    parser.add_argument("-v", "--verbose", action="count",
                        help="increase output verbosity")
    parser.add_argument("-q", "--quiet", action="store_true",
                        help="suppress non-fatal output")
    parser.add_argument("--host", help="TiVo hostname or IP address")
    parser.add_argument("--port", type=int, help="TiVo Remote Protocol port number")
    parser.add_argument("--timeout", type=float,
                        help="socket timeout in seconds (0 = no timeout)")
    parser.add_argument("--ircode", dest="cmd", action='store_const', const='ircode',
                        help="send one or more IR codes.")
    parser.add_argument("--keyboard", dest="cmd", action='store_const', const='keyboard',
                        help="send one or more keyboard codes.")
    parser.add_argument("--teleport", dest="cmd", action='store_const', const='teleport',
                        help="switch to a defined screen (TIVO, LIVETV, NOWPLAYING or GUIDE).")
    parser.add_argument("--get-channel", dest="cmd", action='store_const', const='getch',
                        help="get the currnently selected channel (if any).")
    parser.add_argument("--set-channel", dest="cmd", action='store_const', const='setch',
                        help="switch to a new channel number.")
    parser.add_argument("params", nargs="*",
                        help="parameters for the selected command (key or ir codes,\
                              a screen or channel)")

    args = parser.parse_args()
    log_level = get_log_level(args)
    logging.basicConfig(format="%(message)s", level=log_level)

    config = {}
    config.update({k: v for k, v in vars(args).items() if v is not None})

    if 'host' not in config:
        logging.error("error: --host must be set")
        return

    try:
        remote = Remote(config)
        if args.cmd == "ircode":
            for code in args.params:
                remote.send_ircode(code)
        elif args.cmd == 'keyboard':
            for key in args.params:
                remote.send_keyboard(key)
        elif args.cmd == 'teleport':
            remote.teleport(args.params[0])
        elif args.cmd == 'getch':
            print("{0}".format(remote.channel))
        elif args.cmd == 'setch':
            remote.set_channel(args.params[0])
        elif not args.params:
            logging.warning("error: no parameters provided.")
    except socket.timeout:
        logging.error("error: timeout")
    except OSError as oserr:
        logging.error("error: %s", oserr.strerror)


if __name__ == "__main__":
    main()
