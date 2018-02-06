import argparse
import logging
import socket

from . import __doc__ as doc
from . import __title__ as title
from . import __version__ as version
from . import Remote

def main():
    parser = argparse.ArgumentParser(prog=title, description=doc,
                                     epilog="e.g. %(prog)s --host 192.168.0.10 --ircode CHANNELUP")
    parser.add_argument("--version", action="version",
                        version="%(prog)s {0}".format(version))
    parser.add_argument("-v", "--verbose", action="count",
                        help="increase output verbosity")
    parser.add_argument("-q", "--quiet", action="store_true",
                        help="suppress non-fatal output")
    parser.add_argument("-i", "--interactive", action="store_true",
                        help="interactive control")
    parser.add_argument("--host", help="TiVo hostname or IP address")
    parser.add_argument("--port", type=int, help="TiVo Remote Protocol port number")
    parser.add_argument("--timeout", type=float,
                        help="socket timeout in seconds (0 = no timeout)")
    parser.add_argument("command",
                        help="one of IRCODE, KEYBOARD, TELEPORT or SETCH")
    parser.add_argument("key", nargs="*",
                        help="keys to be sent (e.g. KEY_VOLDOWN)")

    args = parser.parse_args()

    if args.quiet:
        log_level = logging.ERROR
    elif not args.verbose:
        log_level = logging.WARNING
    elif args.verbose == 1:
        log_level = logging.INFO
    else:
        log_level = logging.DEBUG

    logging.basicConfig(format="%(message)s", level=log_level)

    config = {}
    config.update({k: v for k, v in vars(args).items() if v is not None})

    if not 'host' in config:
        logging.error("error: --host must be set")
        return

    try:
        remote = Remote(config)
        if args.command == "IRCODE":
            for key in args.key:
                remote.send_ircode(key)
        elif args.command == 'KEYBOARD':
            for key in args.key:
                remote.send_keyboard(key)
        elif args.command == 'TELEPORT':
            remote.teleport(args.key[0])
        elif args.command == 'SETCH':
            remote.set_channel(args.key[0])
        elif len(args.key) == 0:
            logging.warning("Warning: No keys specified.")
    except socket.timeout:
        logging.error("Error: Timed out!")
    except OSError as e:
        logging.error("Error: %s", e.strerror)

if __name__ == "__main__":
    main()
