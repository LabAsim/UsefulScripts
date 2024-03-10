import os

from parser import parse_arguments
from helper import shutdown_node_gracefully

if __name__ == "__main__":
    args = parse_arguments()
    os.environ["api_key"] = args.api_key
    shutdown_node_gracefully()
