#!/usr/bin/env python
import logging
import os
import socketserver
import pyfiglet
from colorama import init, Fore
from enum import Enum

LOG_FILE = "datagos.log"
HOST, PORT = "0.0.0.0", 9999

logging.basicConfig(level=logging.INFO, format="%(message)s", datefmt="", filename=LOG_FILE, filemode="a")


def banner():
    ascii_art = pyfiglet.figlet_format("DataGos", font="roman", width=150)
    print(ascii_art)


class TagColor(Enum):
    ERROR = "<11>"
    WARNING = "<12>"
    INFO = "<14>"
    DEBUG = "<15>"


class ColorTag(Enum):
    ERROR = Fore.RED
    WARNING = Fore.YELLOW
    INFO = Fore.CYAN
    DEBUG = Fore.MAGENTA


class LogPrinter:
    _occupancy_banner = 12
    _terminal_size = 65

    def __init__(self):
        # size = os.get_terminal_size()
        self._remaining_lines = self._terminal_size - self._occupancy_banner

    def detect_color(self, log_string):
        color = Fore.RESET
        for tag in TagColor:
            if tag.value in log_string:
                color = ColorTag[tag.name]
                return color.value
        return color.value

    def print(self, data: str):
        max_chars = 160
        occupancy_lines = (len(data) // max_chars) + round(len(data) / max_chars)

        self._remaining_lines -= occupancy_lines
        if self._remaining_lines <= 0:
            os.system('clear')
            banner()

            self._remaining_lines = self._terminal_size - self._occupancy_banner
            self._remaining_lines -= occupancy_lines

        color = self.detect_color(log_string=data)
        print(color + data + str(self._remaining_lines))


printer = LogPrinter()


class SyslogUDPHandler(socketserver.BaseRequestHandler):

    def handle(self):
        data = bytes.decode(self.request[0].strip())
        data = data.rstrip("\x00")
        remote_address = f"{self.client_address[0]}:{self.client_address[1]}"
        data_log = f"{remote_address} {data}"
        logging.info(data_log)
        printer.print(data=data)


if __name__ == "__main__":
    init(autoreset=True)
    banner()
    try:
        server = socketserver.UDPServer((HOST, PORT), SyslogUDPHandler)
        server.serve_forever(poll_interval=0.5)

    except (IOError, SystemExit):
        raise
    except KeyboardInterrupt:
        print("Crtl+C Pressed. Shutting down.")
