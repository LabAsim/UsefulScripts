import logging
import os
import socket
import sys
import time

import docker
from Spectrum_docker.formatter import set_logging_level
from Spectrum_docker.parser import parse_arguments
from Spectrum_docker.helper import replace_ip_in_config_env, start_dockercompose, stop_containers

logger = logging.getLogger()

if __name__ == "__main__":
    args = parse_arguments()
    DEBUG, ROOT_PATH = args.debug, args.path
    set_logging_level(debug=DEBUG)

    logger.debug(f"{DEBUG=},\t{ROOT_PATH=}")



hostname = socket.gethostname()

ip_address = socket.gethostbyname(hostname)
logger.debug(f"Hostname: {hostname}")
logger.debug(f"IP Address: {ip_address}")

if __name__ == "__main__":
    replace_ip_in_config_env(path=ROOT_PATH, ip=ip_address)
    #
    try:
        client = docker.from_env()
        logger.debug(f"{client.containers.list()=}")
    except docker.errors.DockerException as err:
        logger.error(f"{err}")
        time.sleep(5)
        sys.exit()
    #os.system(r'start "" "C:\Program Files\Docker\Docker\Docker Desktop.exe"') # dockerd.exe
    #os.system(r'start "" "C:\Program Files\Docker\Docker\resources\dockerd.exe"')
    # 'C:\Program Files\Docker\Docker\DockerCli.exe' -SwitchDaemon & docker-compose up
    stop_containers()
    start_dockercompose(path=ROOT_PATH)
