import logging.handlers
import traceback
from datagos_logger import DataGosLogger, attach_datagos

if __name__ == '__main__':
    LOGGER = DataGosLogger(name="DataGosDemo",
                           level=logging.DEBUG,
                           datagos_server_ip="127.0.0.1",
                           force_stdout=False).get_logger()
    try:
        #attach_datagos()
        LOGGER.info("aaa----------------------------------------------------------")
        #LOGGER.warning("aaa")
        #LOGGER.error("aaa")
        #LOGGER.debug("aaa")

    except Exception as error_message:
        trace = traceback.format_exc()
        LOGGER.error(msg=f"{error_message}\", \"trace\":\"{trace}")
