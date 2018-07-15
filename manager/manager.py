import logging
import re
import sys
from config_reader import ConfigReader
from app_launcher import app_launcher

logging.basicConfig()
logger = logging.getLogger(__file__)
logger.setLevel(logging.DEBUG)


def detect_ssid():
    import subprocess
    interface_info = subprocess.check_output("netsh wlan show interfaces")
    regx = re.search('(?<=SSID                   : ).\S*', interface_info)
    if regx:
        logger.info("Connected to {} network".format(regx.group(0)))
        return regx.group(0)
    return None


if __name__ == "__main__":
    logger.info("Manager Started...")

    logger.info("Initializing data...")
    current_location = None
    config_reader = ConfigReader()

    logger.info("Checking User Input...")
    if sys.argv and len(sys.argv) == 2:
        logger.info("Location details provided: {}".format(sys.argv[1]))
        if sys.argv[1] in config_reader.supported_places:
            logger.info("Provided location is supported, proceeding further...")
            current_location = sys.argv[1]
        else:
            logger.error("Given location is not supported, will try to detect.")
    else:
        logger.info("Location details are not provided, will try to detect.")

    if not current_location:
        connected_network = detect_ssid()
        current_location = config_reader.get_place_with_given_network(connected_network)
        logger.info("Based on connected network identified place is {}.".format(current_location))

    logger.info("Location: {}".format(current_location))
    supported_app_for_location = config_reader.get_supported_apps_for_place(current_location)
    logger.info(supported_app_for_location)
    app_launcher.start_up_manager(supported_app_for_location)

    logger.info("Manager has done his job, not going to relax a bit, enjoy your day... :-)")
