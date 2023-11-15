import logging
import os.path
import pathlib
import re

from Spectrum_docker.constants import ergo_dex_containers

logger = logging.getLogger(__name__)


def replace_ip_in_config_env(*, path: str | pathlib.Path, ip: str) -> None:
    """Replaces the ip in the config.env"""
    path_config_env = os.path.join(path, "config.env")

    line = None

    with open(path_config_env, "r+", encoding="utf-8") as file:
        line = file.readline()
        logger.debug(f"{line=}")

    line = find_replace_ip_in_line(line=line, ip=ip)
    with open(path_config_env, "w+", encoding="utf-8") as file:
        file.write(line)


def find_replace_ip_in_line(*, line: str, ip: str) -> str:
    """Replaces the IP address in the line"""
    ip_pattern = re.compile(r'(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})')
    line = ip_pattern.sub(repl=ip, string=line)
    logger.debug(f"{line=}")
    return line


def stop_containers() -> None:
    """
    Stops the containers from ergo-dex-backend
    There is no need to catch errors when a container does not exist.
    They will be re-created
    """
    for container in ergo_dex_containers:
        os.system(f"docker stop {container}")


def start_dockercompose(path: str | pathlib.Path) -> None:
    """Starts docker-compose"""

    os.system(f"cd {path} && docker-compose up -d")
