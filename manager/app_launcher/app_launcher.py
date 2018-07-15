import os
import sys
import logging

logging.basicConfig()
logger = logging.getLogger(__file__)
logger.setLevel(logging.DEBUG)


def start_apps(app_name):
    os.startfile(app_name)


def start_up_manager(list_of_apps):
    logger.info("Going to start apps -> {}".format(list_of_apps))
    for app in list_of_apps:
        logger.info("Starting {}".format(app))
        start_apps(app)
        logger.info("{} Started successfully".format(app))
    logger.info("All the apps are started")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        logger.error("Invalid parameter")
        exit(0)
    start_up_manager(sys.argv[1])
