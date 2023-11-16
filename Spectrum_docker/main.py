import logging
import socket
import sys
import time
import docker
from Spectrum_docker.formatter import set_logging_level
from Spectrum_docker.parser import parse_arguments
from Spectrum_docker.helper import (
    replace_ip_in_config_env,
    start_dockercompose,
    stop_containers,
    check_node, check_if_node_is_running, find_local_ip
)

logger = logging.getLogger()


def main() -> None:
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
        logger.info(f"Sleeping for {secs=}")
        time.sleep(secs)

    while not check_node():
        logger.error("The node is not synced")
        time.sleep(5)

    try:
        client = docker.from_env()
        logger.debug(f"{client.containers.list()=}")
    except docker.errors.DockerException as err:
        logger.error(f"{err}")
        time.sleep(5)
        sys.exit()
        
    stop_containers()
    start_dockercompose(path=ROOT_PATH)


if __name__ == "__main__":
    main()
