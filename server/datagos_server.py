#!/usr/bin/env python
import json
import logging
import os
import socketserver
from typing import Any

import pyfiglet
from colorama import init, Fore
from enum import Enum

from domain.trace.datagos_trace import DatagosTrace
from infrastructure.persistence.mysql_client import get_mysql_client
from infrastructure.persistence.mysql_datagos import MySqlDatagosRepository

LOG_FILE = "datagos.log"
HOST, PORT = "0.0.0.0", 39999

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

    def print_to_custom_terminal(self, data: str):
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

    def print_to_std_terminal(self, data: str):
        color = self.detect_color(log_string=data)
        print(color + data)


printer = LogPrinter()


class SyslogUDPHandler(socketserver.BaseRequestHandler):
    _datagos_repo = MySqlDatagosRepository(db_client=get_mysql_client())

    def handle(self):
        data = None
        try:
            remote_address = f"{self.client_address[0]}:{self.client_address[1]}"
            if self.request[0].strip()[0] == 0xd0:
                print(f"Detected 0xd0 from {remote_address} -> {self.request[0].strip()}")
                return

            data = bytes.decode(self.request[0].strip())
            data = data.rstrip("\x00")

            data_log = f"{remote_address} {data}"
            logging.info(data_log)

            sanitize = data.replace('"{"', '{"').replace('}"}', '}}')
            printer.print_to_std_terminal(data=sanitize)
            data = json.loads(sanitize[4:])
        except Exception as e:
            trace = {"error": str(e), "request0": str(self.request[0]), "request": self.request}
            datagos_trace = DatagosTrace(trace=trace,
                                         type="ERROR",
                                         service_name="Datagos.SyslogUDPHandler",
                                         )
            print(f"Exception trace: {trace}\ndatagos_trace: {datagos_trace}")
            # self._datagos_repo.save(trace=datagos_trace)
            data = None

        if data is None:
            print(f"self.request: {self.request}")
            print(f"self.request0: {self.request[0]}")
            return

        datagos_trace = DatagosTrace(trace=data,
                                     type=data.get("level") or "no_type",
                                     service_name=data.get("name") or "no_service",
                                     )
        self._datagos_repo.save(trace=datagos_trace)

    def get_data_safe(self, raw: Any) -> Any:
        try:
            data = bytes.decode(raw[0].strip())
            data = data.rstrip("\x00")
        except Exception as e:
            data = {
                "service_name": "get_data_safe",
                "type": logging.ERROR,
                "message": "cannot get data safely",
                "message_exception": str(e),
                "data_raw": raw,
            }
        return data


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
