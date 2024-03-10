import argparse


def parse_arguments() -> argparse.ArgumentParser.parse_args:
    """
    Parser for commandline arguments.
    :return: my_parser.parse_args()
    """
    my_parser = argparse.ArgumentParser()
    my_parser.add_argument(
        "--debug",
        type=str2bool,
        action="store",
        const=True,
        nargs="?",
        required=False,
        default=True,
        help="If True, it prints everything set to DEBUG and above.",
    )
    my_parser.add_argument(
        "--path",
        type=str,
        action="store",
        const=True,
        nargs="?",
        required=False,
        default="C:\\ergo_spectrum\\ergo-dex-backend",
        help="The patch to ergo-dex-backend",
    )
    my_parser.add_argument(
        "--api_key",
        type=str,
        action="store",
        const=True,
        nargs="?",
        required=False,
        default="1234",
        help="The api key of the node",
    )
    my_parser.add_argument(
        "--jar_version",
        type=str,
        action="store",
        const=True,
        nargs="?",
        required=False,
        default="5.0.1",
        help="The jar version of the node",
    )
    return my_parser.parse_args()


def str2bool(v: bool | int | str) -> bool:
    """
    Convert a string to a boolean argument
    https://stackoverflow.com/questions/15008758/parsing-boolean-values-with-argparse
    """
    if isinstance(v, bool):
        return v
    elif isinstance(v, int):
        if v == 1:
            return True
        elif v == 0:
            return False
    elif v.lower() in ("yes", "true", "t", "y", "1"):
        return True
    elif v.lower() in ("no", "false", "f", "n", "0"):
        return False
    else:
        raise TypeError("Boolean or equivalent value expected.")
