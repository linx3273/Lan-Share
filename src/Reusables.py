from rich.console import Console
from pathlib import Path
import os

INF_COLOR = "bold green"
INP_COLOR = "bold yellow"
WAR_COLOR = "yellow"
ERR_COLOR = "red"

ADDR_STYLE = "bold blue"

CWD = Path(os.getcwd()).resolve().as_posix()

MODE = ["sender", "receiver"]


class Msgs:

    def __init__(self):
        self._console = Console()

    def inf(self):
        """
        Prints [INF] in green
        :return:
        """
        print("[", end='')
        self._console.print("INF", style=INF_COLOR, end="")
        print("]", end=" ")

    def inp_msg(self):
        """
        Prints [INP] in bold yellow
        :return:
        """
        print("[", end='')
        self._console.print("INP", style=INP_COLOR, end="")
        print("]", end=" ")

    def warn_msg(self):
        """
        Prints [WAR] in yellow
        :return:
        """
        print("[", end='')
        self._console.print("WAR", style=WAR_COLOR, end="")
        print("]", end=" ")

    def err_msg(self):
        """
        prints [ERR] in Red
        :return:
        """
        print("[", end='')
        self._console.print("ERR", style=ERR_COLOR, end="")
        print("]", end=" ")

    def console(self):
        """
        Allows user to print Rich statements by accessing the instance console
        :return:
        """
        return self._console
