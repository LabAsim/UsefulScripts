import logging
import os.path
import pathlib
import re
import socket
import subprocess

import requests
import json
import urllib3

from Spectrum_docker.constants import ergo_dex_containers

logger = logging.getLogger(__name__)


def find_local_ip() -> str:
    """
    Finds and returns the local ip (192.XXX..)
    # https://stackoverflow.com/a/166520
    # See comments for clarification
    """
    hostname = socket.gethostname()
    # ip_address = socket.gethostbyname_ex(hostname)[-1][-1]
    ips = [
        ip for ip in socket.gethostbyname_ex(socket.gethostname())[2] if
        (
                not ip.startswith("127.") and not ip.startswith("172.")
        )
    ]
    if len(ips) > 1:
        logger.warning(f"Too many {ips=}")
        logger.warning(f"Picking the last one {ips[-1]=}")

    return ips[-1].strip()


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
        # os.system(f"docker stop {container}")
        a = subprocess.run([f"docker", "stop", f"{container}"], capture_output=True)
        name = str(a.stdout.decode(encoding='utf-8')).strip("\n")
        logger.debug(f"Container {name=} stopped")


def delete_containers() -> None:
    """
    The containers must be deleted to avoid error
    `error from daemon in stream: Error grabbing logs: invalid character '\x00' looking for beginning of value`
    See: https://github.com/docker/for-linux/issues/140
    """
    for container in ergo_dex_containers:
        # os.system(f"docker rm --force {container}")
        a = subprocess.run([f"docker", "rm", "--force", f"{container}"], capture_output=True)
        name = str(a.stdout.decode(encoding='utf-8')).strip("\n")
        logger.debug(f"Container {name=} deleted")


def start_dockercompose(path: str | pathlib.Path) -> None:
    """Starts docker-compose"""

    path = pathlib.WindowsPath(path)
    a = subprocess.run(["cd", path,  "&&", "docker-compose", "up", "-d"], capture_output=True, shell=True)
    #logger.debug(f"Called {a=}")
    for line in a.stderr.split(b"\n"):
        logger.debug(f"{line.decode(encoding='utf-8').strip()}")


def check_node() -> bool:
    """Checks if the node is synced"""
    url = 'http://127.0.0.1:9053/info'
    headers = {'accept': 'application/json'}
    req = requests.get(url, headers=headers)
    info = json.loads(req.text)
    fullheight = info["fullHeight"]
    maxPeerHeight = info["maxPeerHeight"]
    stateVersion = info["stateVersion"]
    bestFullHeaderId = info["bestFullHeaderId"]
    bestHeaderId = info["bestHeaderId"]
    logger.info(f"{fullheight=} {maxPeerHeight=} {stateVersion=} {bestHeaderId=} {bestFullHeaderId=}")
    # Avoid Nones and match the version with the network block ID
    if (stateVersion and bestHeaderId and bestFullHeaderId) and stateVersion == bestFullHeaderId:
        return True
    return False


def check_if_node_is_running() -> bool:
    """Checks if the node is up"""
    url = "http://127.0.0.1:9053/info"
    try:
        requests.get(url)
    except (requests.exceptions.ConnectionError, urllib3.exceptions.NewConnectionError) as err:
        logger.error(f"Cannot reach the node at {url=}")
        return False

    return True
