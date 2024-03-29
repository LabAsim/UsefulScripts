import logging
import os.path
import pathlib
import re
import socket
import subprocess
import threading
import time
import psutil
from functools import wraps
from typing import Callable

import requests
import json
import urllib3
import constants
from constants import ergo_dex_containers

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

    lines = None

    with open(path_config_env, "r+", encoding="utf-8") as file:
        # Read the whole text at once
        # Not each line seperately
        lines = file.read()
        logger.debug(f"{lines=}")

    lines = find_replace_ip_in_line(line=lines, ip=ip)

    logger.debug(f"{lines=}")

    with open(path_config_env, "w+", encoding="utf-8") as file:
        file.write(lines)


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
    a = subprocess.run(["cd", path, "&&", "docker-compose", "up", "-d"], capture_output=True, shell=True)
    # logger.debug(f"Called {a=}")
    for line in a.stderr.split(b"\n"):
        logger.debug(f"{line.decode(encoding='utf-8').strip()}")


def start_node(path: str | pathlib.Path, ram_gb: int, jar_version: str) -> None:
    """Starts the node given the path"""
    # We don't use Windows path here, because we use powershell in subprocess
    path = pathlib.PurePosixPath(path)
    subprocess.Popen(
        args=
        [
            "cd", path, "&&", "java", f"-Xmx{ram_gb}g", "-jar", f"ergo-{jar_version}.jar", "--mainnet", "-c", "ergo"
                                                                                                              ".conf"
        ],
        shell=True,
        stderr=subprocess.DEVNULL,
        stdin=subprocess.DEVNULL,
        stdout=subprocess.DEVNULL,
        close_fds=True
    )
    logger.info(f"The node started at {path=}")


def start_node_thread(path: str | pathlib.Path, ram_gb: int,  jar_version: str) -> None:
    """Start the node in a separate thread after checking if a node is already running"""
    if not check_if_node_is_running():
        thr = threading.Thread(target=start_node, args=(
            path,
            ram_gb,
            jar_version
        ))
        thr.start()
        logger.info(f"Node started at {path =} with {ram_gb=}")


def check_if_node_is_running() -> bool:
    """Checks if the node is up"""
    url = "http://127.0.0.1:9053/info"
    try:
        requests.get(url)
    except (
            requests.exceptions.ConnectionError,
            urllib3.exceptions.NewConnectionError,
    ):
        logger.error(f"Cannot reach the node at {url=}")
        return False

    return True


def loop_check_node_is_running(func: Callable) -> Callable:
    """A decorator which checks if the node is running"""

    @wraps(func)
    def inner_func(*args, **kwargs) -> None:
        """
        Inner function which first checks
        if the node is running and then executes the func
        """
        # if not check_if_node_is_running():
        #     start_node(
        #         path=constants.PATH,
        #         ram_gb=constants.RAM_GB
        #     )
        while not check_if_node_is_running():
            start_node(
                path=constants.PATH,
                ram_gb=constants.RAM_GB,
                jar_version=constants.JAR_VERSION
            )
            secs = 3
            logger.warning(f"Node is not running. Sleeping for {secs=}")
            time.sleep(secs)

        logger.info(f"Node is running")
        return func(*args, **kwargs)

    return inner_func


@loop_check_node_is_running
def check_node_sync() -> bool:
    """Checks if the node is synced"""
    url = 'http://127.0.0.1:9053/info'
    headers = {'accept': 'application/json'}
    req = requests.get(url, headers=headers)
    info = json.loads(req.text)
    fullheight = info["fullHeight"]
    maxPeerHeight = info["maxPeerHeight"]
    logger.debug(f"{fullheight=}")
    logger.debug(f"{maxPeerHeight=}")
    if (fullheight == maxPeerHeight) and \
            (fullheight is not None) and \
            (maxPeerHeight is not None):
        return True
    return False


def shutdown_node_gracefully() -> None:
    """Make a post req to the node to shut down gracefully"""
    requests.post(
        "http://127.0.0.1:9053/node/shutdown",
        headers={
            'accept': 'application/json',
            "api_key": os.getenv(key="api_key", default="1234")
        }
    )


def kill_itself() -> None:
    """Get the parent pid and kill recursively all the children processes"""
    pid = os.getppid()
    children = psutil.Process(pid).children(recursive=True)
    for child in children:
        process_info = child.as_dict(attrs=['name', 'pid'])
        os.kill(process_info["pid"], 9)
        logger.debug(f"{process_info['name']=}({process_info['pid']}) killed")
    os.kill(pid, 9)