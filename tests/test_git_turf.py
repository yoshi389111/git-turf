#!/usr/bin/env python

import argparse
import doctest
import unittest
from datetime import date, datetime, time
from unittest.mock import call, patch

import git_turf.git_turf as git_turf


class TestGitTurf(unittest.TestCase):
    def test_sunday_a_year_ago(self):
        self.assertEqual(
            date(2018, 8, 5), git_turf.sunday_a_year_ago(date(2019, 8, 10))
        )
        self.assertEqual(
            date(2018, 8, 12), git_turf.sunday_a_year_ago(date(2019, 8, 11))
        )
        self.assertEqual(
            date(2018, 8, 12), git_turf.sunday_a_year_ago(date(2019, 8, 17))
        )
        self.assertEqual(
            date(2018, 8, 19), git_turf.sunday_a_year_ago(date(2019, 8, 18))
        )

    def test_read_fonts(self):
        fonts = git_turf.read_fonts()
        self.assertEqual(b"\x00\x00\x00", fonts[" "])
        self.assertEqual(b"\x7f\x08\x08\x08\x7f\x00", fonts["H"])
        self.assertEqual(b"\x7f\x04\x08\x10\x7f\x00", fonts["N"])

    def test_convert_bitmap(self):
        fonts = {"a": b"\xaa", "b": b"\xbb\xbb", "c": b"\xcc\xcc\xcc"}
        self.assertEqual(
            b"\xaa\xbb\xbb\xcc\xcc\xcc", git_turf.convert_bitmap(fonts, "abc")
        )

    def test_show_bitmap(self):
        pass  # doctest

    def test_target_days(self):
        self.assertEqual(
            [0, 2, 4, 5, 6, 7, 10], list(git_turf.target_days(b"\x75\x09"))
        )

    @patch("subprocess.check_call")
    def test_do_commit(self, mock_subprocess):
        git_turf.do_commit(datetime(1990, 1, 2, 12, 34, 56))
        mock_subprocess.assert_called_once_with(
            [
                "git",
                "commit",
                "-qm",
                "_",
                "--allow-empty",
                "--date=1990-01-02T12:34:56",
            ]
        )

    @patch("git_turf.git_turf.do_commit")
    def test_commit_message(self, mock_do_commit):
        git_turf.commit_message(datetime(1980, 1, 1, 23, 59, 58), b"\x75\x09")
        self.assertEqual(
            [
                call(datetime(1980, 1, 1, 23, 59, 58)),
                call(datetime(1980, 1, 3, 23, 59, 58)),
                call(datetime(1980, 1, 5, 23, 59, 58)),
                call(datetime(1980, 1, 6, 23, 59, 58)),
                call(datetime(1980, 1, 7, 23, 59, 58)),
                call(datetime(1980, 1, 8, 23, 59, 58)),
                call(datetime(1980, 1, 11, 23, 59, 58)),
            ],
            mock_do_commit.call_args_list,
        )

    def test_valid_date(self):
        self.assertEqual(date(2019, 1, 1), git_turf.valid_date("2019-01-01"))
        with self.assertRaises(argparse.ArgumentTypeError):
            git_turf.valid_date("2019/01/01")

    def test_valid_time(self):
        self.assertEqual(time(12, 34, 56), git_turf.valid_time("12:34:56"))

        with self.assertRaises(argparse.ArgumentTypeError):
            git_turf.valid_time("12:34:56.000")

    @patch("git_turf.git_turf.commit_message")
    @patch("git_turf.git_turf.show_bitmap")
    @patch("git_turf.git_turf.convert_bitmap", return_value=b"\x00\x7f")
    @patch("git_turf.git_turf.read_fonts", return_value={})
    def test_git_tuf(self, mock_read, mock_convert, mock_show, mock_commit):
        git_turf.git_turf("test", date(2000, 2, 3), time(11, 22, 33), False)
        self.assertEqual(1, mock_read.call_count)
        mock_convert.assert_called_once_with({}, "test")
        mock_show.assert_called_once_with(b"\x00\x7f")
        mock_commit.assert_called_once_with(
            datetime(2000, 2, 3, 11, 22, 33), b"\x00\x7f"
        )

    def test_arg_parser(self):
        parser = git_turf.arg_parser(datetime(2001, 2, 3, 11, 22, 33))

        args1 = parser.parse_args(["hello1"])
        self.assertEqual("hello1", args1.MESSAGE)
        self.assertEqual(date(2000, 1, 30), args1.date)
        self.assertEqual(time(11, 22, 33), args1.time)
        self.assertFalse(args1.dry_run)

        args2 = parser.parse_args(["-d", "1999-03-03", "HELLO2"])
        self.assertEqual("HELLO2", args2.MESSAGE)
        self.assertEqual(date(1999, 3, 3), args2.date)
        self.assertEqual(time(11, 22, 33), args2.time)
        self.assertFalse(args2.dry_run)

        args3 = parser.parse_args(["--date", "1998-04-04", "Hello3"])
        self.assertEqual("Hello3", args3.MESSAGE)
        self.assertEqual(date(1998, 4, 4), args3.date)
        self.assertEqual(time(11, 22, 33), args3.time)
        self.assertFalse(args3.dry_run)

        args4 = parser.parse_args(["-t", "10:20:30", "hello4"])
        self.assertEqual("hello4", args4.MESSAGE)
        self.assertEqual(date(2000, 1, 30), args4.date)
        self.assertEqual(time(10, 20, 30), args4.time)
        self.assertFalse(args4.dry_run)

        args5 = parser.parse_args(["--time", "01:02:03", "hello5"])
        self.assertEqual("hello5", args5.MESSAGE)
        self.assertEqual(date(2000, 1, 30), args5.date)
        self.assertEqual(time(1, 2, 3), args5.time)
        self.assertFalse(args5.dry_run)

        args6 = parser.parse_args(["-n", "hello6"])
        self.assertEqual("hello6", args6.MESSAGE)
        self.assertEqual(date(2000, 1, 30), args6.date)
        self.assertEqual(time(11, 22, 33), args6.time)
        self.assertTrue(args6.dry_run)

        args7 = parser.parse_args(["--dry-run", "hello7"])
        self.assertEqual("hello7", args7.MESSAGE)
        self.assertEqual(date(2000, 1, 30), args7.date)
        self.assertEqual(time(11, 22, 33), args7.time)
        self.assertTrue(args7.dry_run)


def load_tests(loader, tests, ignore):
    tests.addTests(doctest.DocTestSuite(git_turf))
    return tests


if __name__ == "__main__":
    unittest.main()
