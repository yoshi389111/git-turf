#!/usr/bin/env python3
# Copyright (C) 2019, SATO_Yoshiyuki
# This software is released under the MIT License.
# http://opensource.org/licenses/mit-license.php


import argparse
import subprocess
from datetime import date, datetime, time, timedelta
from typing import Dict, Iterable

from . import font_data

_name = "git-turf"
_version = "0.1.0"
_license = "MIT License"
_description = (
    "The git-turf program outputs ASCII art to GitHub contribution graph"
)
_url = "https://github.com/yoshi389111/git-turf"
_author = "yoshi389111"
_author_email = "yoshi.389111@gmail.com"


def sunday_a_year_ago(today: date) -> date:
    """
    >>> sunday_a_year_ago(date(2019, 8, 4))
    datetime.date(2018, 8, 5)
    """
    days_ago = today.isoweekday() % 7 + 52 * 7
    return today - timedelta(days=days_ago)


def read_fonts() -> Dict[str, bytes]:
    return font_data.create()


def convert_bitmap(fonts: Dict[str, bytes], message: str) -> bytes:
    bitmap = bytearray()
    for ch in message:
        if ch in fonts:
            bitmap += fonts[ch]
    return bytes(bitmap)


def show_bitmap(bitmap: bytes) -> None:
    """
    >>> show_bitmap(bytes.fromhex("7f0408107f007f0808087f"))
    #   # #   #
    #   # #   #
    ##  # #   #
    # # # #####
    #  ## #   #
    #   # #   #
    #   # #   #
    """
    for i in range(7):
        mask = 1 << i
        for b in bitmap:
            ch = "#" if b & mask else " "
            print(ch, end="")
        print()


def target_days(bitmap: bytes) -> Iterable[int]:
    days = 0
    for b in bitmap:
        for i in range(7):
            if b & (1 << i):
                yield days
            days += 1


def do_commit(commit_datetime: datetime) -> None:
    command = [
        "git",
        "commit",
        "-qm",
        "_",
        "--allow-empty",
        "--date={}".format(commit_datetime.isoformat()),
    ]
    subprocess.check_call(command)


def commit_message(start_datetime: datetime, bitmap: bytes) -> None:
    for days in target_days(bitmap):
        commit_datetime = start_datetime + timedelta(days=days)
        do_commit(commit_datetime)


def valid_date(s: str) -> date:
    """
    >>> valid_date("2019-01-01")
    datetime.date(2019, 1, 1)
    >>> valid_date("2019/01/01")
    Traceback (most recent call last):
     ...
    argparse.ArgumentTypeError: Not a valid date: '2019/01/01'.

    """
    try:
        return datetime.strptime(s, "%Y-%m-%d").date()
    except ValueError:
        msg = "Not a valid date: '{0}'.".format(s)
        raise argparse.ArgumentTypeError(msg)


def valid_time(s: str) -> time:
    """
    >>> valid_time("12:34:56")
    datetime.time(12, 34, 56)
    >>> valid_time("12:34:56.000")
    Traceback (most recent call last):
     ...
    argparse.ArgumentTypeError: Not a valid time: '12:34:56.000'.
    """

    try:
        return datetime.strptime(s, "%H:%M:%S").time()
    except ValueError:
        msg = "Not a valid time: '{0}'.".format(s)
        raise argparse.ArgumentTypeError(msg)


def main() -> None:
    now = datetime.now().replace(microsecond=0)
    start_date = sunday_a_year_ago(now.date())

    parser = argparse.ArgumentParser(description=_description)
    parser.add_argument(
        "MESSAGE", help="message output to GitHub contribution graph"
    )
    parser.add_argument(
        "-v",
        "--version",
        action="version",
        version="{} {}".format(_name, _version),
    )
    parser.add_argument(
        "-d",
        "--date",
        type=valid_date,
        help="start date. format is YYYY-MM-DD",
        default=start_date,
    )
    parser.add_argument(
        "-t",
        "--time",
        type=valid_time,
        help="commit time. format is HH:MM:SS",
        default=now.time(),
    )
    parser.add_argument(
        "-n",
        "--dry-run",
        action="store_true",
        default=False,
        help="display message only",
    )

    args = parser.parse_args()

    fonts = read_fonts()
    bitmap = convert_bitmap(fonts, args.MESSAGE)

    show_bitmap(bitmap)

    if not args.dry_run:
        start_datetime = datetime.combine(args.date, args.time)
        commit_message(start_datetime, bitmap)


if __name__ == "__main__":
    main()
