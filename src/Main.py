import Host
import Client
import argparse
import re
import Reusables
import sys
from pathlib import Path
import os


msgs = Reusables.Msgs()
IP_PORT_MATCH = "^(([0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5])\.){3}([0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5]):[0-9]+$"


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        prog=f"{Path(sys.argv[0]).name}",
        description="Share files on local area network",
        epilog="Source code at https://github.com/linx3273/Lan-Share"
    )

    group = parser.add_mutually_exclusive_group()
    group.add_argument("--host", help="Run program as a host", action="store_true")
    group.add_argument("--client", help="Run program as a client", action="store_true")

    parser.add_argument("path", help="Path of directory to send/receive in or path of file to be sent")
    parser.add_argument("ip", help="IP:PORT of host to which the client must be connected (Required if using --client)",
                        nargs="?")

    args = parser.parse_args()
    if args.client is None and args.host is None:
        parser.error("Either host or client mode is required")

    elif args.client and args.ip is None:
        parser.error("IP is required when running in client mode")

    elif args.client and not re.search(IP_PORT_MATCH, args.ip):
        msgs.err_msg()
        msgs.console().print("Invalid IP:PORT")

    elif args.client and re.search(IP_PORT_MATCH, args.ip):
        msgs.inf()
        msgs.console().print("Running as a client")
        if os.name == 'nt':
            if args.path[-1] == "'" or args.path[-1] == '"':
                args.path = args.path[:-1]

            c = Client.Client(args.path, args.ip)
        else:
            c = Client.Client(args.path, args.ip)
        c.client()

    elif args.host:
        msgs.inf()
        msgs.console().print("Running as a host")
        if os.name == 'nt':
            if args.path[-1] == "'" or args.path[-1] == '"':
                args.path = args.path[:-1]  
                          
            h = Host.Host(args.path)
        else:
            h = Host.Host(args.path)
        h.host()

    else:
        msgs.err_msg()
        msgs.console().print("You should not be seeing this.")
