import Reusables
from Share import Share
import socket


msgs = Reusables.Msgs()


class Client(Share):
    def __init__(self, path, ip):
        super().__init__(path)
        self._ip = ip  # Stores IP of host to which client will connect

    def parse_ip(self):
        """
        Takes IP:PORT in string format and returns a tuple containing the (IP, int(PORT))
        :return:
        (IP, int(PORT))
        """
        temp = self._ip.split(":")
        return (temp[0], int(temp[1]))

    def client(self):
        self._conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self._conn.connect(self.parse_ip())
        msgs.inf()
        msgs.console().print(f"Connecting to [{Reusables.ADDR_STYLE}]{self._ip}[/{Reusables.ADDR_STYLE}]")

        self.get_mode()
        msgs.inf()
        msgs.console().print(f"Set mode to [yellow]{self._mode}[/yellow]")
        self.transfer_handler()
        self._conn.close()
