import argparse


def parse_arguments() -> argparse.ArgumentParser.parse_args:
    """
    Parser for commandline arguments.
    :return: my_parser.parse_args()
    """
    my_parser = argparse.ArgumentParser()
    my_parser.add_argument(
        "--file",
        type=str,
        action="store",
        const=True,
        nargs="?",
        required=False,
        default="math.md",
        help="The file to parse",
    )
    return my_parser.parse_args()
