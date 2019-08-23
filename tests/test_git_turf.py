#!/usr/bin/env python

import argparse
import doctest
import unittest
from datetime import date, time

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
        pass  # TODO

    def test_do_commit(self):
        pass  # TODO

    def test_commit_message(self):
        pass  # TODO

    def test_valid_date(self):
        self.assertEqual(date(2019, 1, 1), git_turf.valid_date("2019-01-01"))

        with self.assertRaises(argparse.ArgumentTypeError):
            git_turf.valid_date("2019/01/01")

    def test_valid_time(self):
        self.assertEqual(time(12, 34, 56), git_turf.valid_time("12:34:56"))

        with self.assertRaises(argparse.ArgumentTypeError):
            git_turf.valid_time("12:34:56.000")


def load_tests(loader, tests, ignore):
    tests.addTests(doctest.DocTestSuite(git_turf))
    return tests


if __name__ == "__main__":
    unittest.main()
