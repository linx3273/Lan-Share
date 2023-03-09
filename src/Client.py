import Reusables
from Share import Share
import socket
import os
from PyInquirer import prompt


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
        
        self.recv_mode_check()
        self.transfer_handler()
        
        msgs.inf()
        msgs.console().print("Connection has been closed.")
        self._conn.close()


    def recv_mode_check(self):
        """
        Checks if the client is in receive mode and the path provided by client is file. In which case
        check with user regarding whether to put file in directory consisting file
        :return:
        """
        if self._mode == Reusables.MODE[1] and os.path.isfile(self._path):
            msgs.warn_msg()
            msgs.console().print(f"Receive path is a file, not directory. Changing path to [yellow]{self._path.parent}[/yellow].")
            self._path = self._path.parent        