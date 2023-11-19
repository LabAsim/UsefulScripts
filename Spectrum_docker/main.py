import logging
import socket
import sys
import time
import colorama
import docker
from Spectrum_docker.formatter import set_logging_level
from Spectrum_docker.parser import parse_arguments
from Spectrum_docker.helper import (
    replace_ip_in_config_env,
    start_dockercompose,
    stop_containers,
    check_node,
    check_if_node_is_running,
    find_local_ip,
    delete_containers,
)
from Spectrum_docker.constants import COLORAMA_TERMINAL_COLORS


logger = logging.getLogger()


def main() -> None:
    colorama.init(convert=COLORAMA_TERMINAL_COLORS)
    args = parse_arguments()
    DEBUG, ROOT_PATH = args.debug, args.path
    set_logging_level(debug=DEBUG)
    logger.debug(f"{DEBUG=},\t{ROOT_PATH=}")

    ip_address = find_local_ip()
    logger.info(f"Hostname: {socket.gethostname()}")
    logger.info(f"IP Address: {ip_address}")
    replace_ip_in_config_env(path=ROOT_PATH, ip=ip_address)

    while not check_if_node_is_running():
        secs = 3
        logger.warning(f"Node is not running. Sleeping for {secs=}")
        time.sleep(secs)
    logger.info(f"Node is running")

    while not check_node():
        logger.warning("The node is not synced")
        time.sleep(5)
    logger.info("Node is synced")

    try:
        client = docker.from_env()
        logger.debug(f"{client.containers.list()=}")
    except docker.errors.DockerException as err:
        logger.critical(f"{err}")
        time.sleep(5)
        sys.exit()

    stop_containers()
    delete_containers()
    start_dockercompose(path=ROOT_PATH)
    logger.info("The script ended")
    time.sleep(3)


if __name__ == "__main__":
    main()
