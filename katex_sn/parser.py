import argparse
from datetime import datetime


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
    my_parser.add_argument(
        "--out",
        type=str,
        action="store",
        const=True,
        nargs="?",
        required=False,
        default="test.pdf",
        help="The name of output file",
    )
    current_dateTime = datetime.now()
    year = current_dateTime.year
    month = current_dateTime.month
    day = current_dateTime.day
    my_parser.add_argument(
        "--date",
        type=str,
        action="store",
        const=True,
        nargs="?",
        required=False,
        default=f"{day}/{month}/{year}",
        help="The file to parse",
    )
    my_parser.add_argument(
        "--title",
        type=str,
        action="store",
        const=True,
        nargs="?",
        required=False,
        default=f"Notes",
        help="The title of the file",
    )

    my_parser.add_argument(
        "--author",
        type=str,
        action="store",
        const=True,
        nargs="?",
        required=False,
        default=f"",
        help="The authors of the file",
    )
    return my_parser.parse_args()
