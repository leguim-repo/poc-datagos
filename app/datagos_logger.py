import json
import logging
import socket
import sys
import logging.handlers


class DataGosLogger(logging.Logger):
    """
    force_stdout=True if you want see in local machine. For AWS Environment should be False
    """

    _log_level_to_name = {
        logging.CRITICAL: "CRITICAL",
        logging.ERROR: "ERROR",
        logging.WARNING: "WARNING",
        logging.INFO: "INFO",
        logging.DEBUG: "DEBUG",
        logging.NOTSET: "NOTSET",
    }

    _log_format = json.dumps({
        "timestamp": "%(asctime)s",
        "level": "%(levelname)s",
        "name": "%(name)s",
        "message": "%(message)s",
    })

    def __init__(self, name: str,
                 level=logging.INFO,
                 force_stdout=False,
                 datagos_server_ip="192.168.0.250",
                 datagos_server_port=39999):
        super().__init__(name, level)
        self.level = level
        self.name = name

        logging.basicConfig(level=self.level, format=self._log_format)

        # Complete logging config.
        self.logger = logging.getLogger(name)
        self.logger.setLevel(self.level)

        _handler_datagos_server(target_logger=self.logger,
                                datagos_server_ip=datagos_server_ip,
                                datagos_server_port=datagos_server_port,
                                log_format=self._log_format)

        if force_stdout:
            self.console_logger = logging.StreamHandler(sys.stdout)
            self.logger.addHandler(self.console_logger)

    def get_logger(self):
        return self.logger


def _handler_datagos_server(target_logger: logging.Logger,
                            datagos_server_ip="192.168.0.250",
                            datagos_server_port=9999,
                            log_format=json.dumps({
                                "timestamp": "%(asctime)s",
                                "level": "%(levelname)s",
                                "name": "%(name)s",
                                "message": "%(message)s",
                            })):
    handler = logging.handlers.SysLogHandler(address=(datagos_server_ip, datagos_server_port),
                                             socktype=socket.SOCK_DGRAM)
    handler.setFormatter(logging.Formatter(fmt=log_format, datefmt='%Y-%m-%dT%H:%M:%S'))

    target_logger.addHandler(handler)


def attach_datagos(logger_blacklist: list = [], attach_to_root_logger: bool = False) -> None:
    """
    Attach DataGos handler to App without use any specific logging
    DataGos is attached to all available loggers in App when this method is called
    :return:
    """

    root_logger = logging.getLogger("root")

    if attach_to_root_logger:
        _handler_datagos_server(root_logger)

    for name in logging.root.manager.loggerDict.keys():
        if name not in logger_blacklist:
            target_logger = logging.getLogger(name)
            _handler_datagos_server(target_logger)

            root_logger.debug(f"Attached DataGos handler to logger named {target_logger.name}")
