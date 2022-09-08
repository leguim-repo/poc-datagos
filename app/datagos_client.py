import json
import logging.handlers
import traceback
from datagos_logger import DataGosLogger, attach_datagos

if __name__ == '__main__':
    local_server = "127.0.01"
    prod_server = "192.168.0.47"
    if True:
        datagos_server_ip = local_server
    else:
        datagos_server_ip = prod_server
    LOGGER = DataGosLogger(name="DataGosDemo",
                           level=logging.DEBUG,
                           datagos_server_ip=datagos_server_ip,
                           force_stdout=False).get_logger()
    try:
        # attach_datagos()
        # LOGGER.info("info")
        # LOGGER.warning("warning")
        # LOGGER.error("error")
        # LOGGER.debug("debug")
        # LOGGER.info("esto pinta que chuta por fin")

        state = {"canal1": 122, "canal2": 222}
        message = {"method": "metodo_chungo", "message": "mensaje del metodo", "estado": state}
        traza_to_datagos = {"message": message}
        LOGGER.info(json.dumps(traza_to_datagos))

    except Exception as error_message:
        trace = traceback.format_exc()
        LOGGER.error(msg=f"{error_message}\", \"trace\":\"{trace}")
