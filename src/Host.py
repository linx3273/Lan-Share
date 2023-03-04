import Reusables
from Share import Share
import socket


msgs = Reusables.Msgs()


class Host(Share):
    def __init__(self, path):
        super().__init__(path)
        self._host = None  # holds the socket bind that will receive connection requests
        self._addr = None  # holds the address of the device that has connected

        self.set_mode()  # check if host wants to send or receive files

    def host(self):
        self._host = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            self._host.bind((socket.gethostbyname(socket.gethostname()), 8000))
        except:
            self._host.bind((socket.gethostbyname(socket.gethostname()), 0))

        self._host.listen()

        msgs.inf()
        msgs.console().print(f"Server listening on [{Reusables.ADDR_STYLE}]{self._host.getsockname()[0]}:{self._host.getsockname()[1]}[/{Reusables.ADDR_STYLE}]")
        self._conn, addr = self._host.accept()

        msgs.inf()
        msgs.console().print(f"[{Reusables.ADDR_STYLE}]{addr[0]}[/{Reusables.ADDR_STYLE}] has connected.")
        self.transfer_handler(host=True)
        self._conn.close()
        self._host.close()
