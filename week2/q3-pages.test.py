import unittest
from unittest.mock import patch
from q3pages import build_index, search

test_case = [
    "8",
    "google code jam is launching",
    "hash code competition results are announced",
    "google launches tech elevate program",
    "code jam final round",
    "youtube newest features",
    "football world cup results",
    "top viewed videos last year",
    "australian open singles results",
    "5",
    "world cup football",
    "results",
    "views",
    "jam code",
    "google program"
]
class PaagesTest(unittest.TestCase):

    # Cool! I learned how to mock builtins with multiple outputs :-D     
    # def test_example(self):
    #     with patch('builtins.input', side_effect=test_case):
    #         q3()

    def test_world_cup_football(self):
        pages = [
            "google code jam is launching",
            "hash code competition results are announced",
            "google launches tech elevate program",
            "code jam final round",
            "youtube newest features",
            "football world cup results",
            "top viewed videos last year",
            "australian open singles results"
        ]
        tree = build_index(pages)
        results = search(tree, "world cup football")
        self.assertEqual(len(results), 1)
        self.assertEqual(results, ["football world cup results"])

    def test_results(self):
        pages = [
            "google code jam is launching",
            "hash code competition results are announced",
            "google launches tech elevate program",
            "code jam final round",
            "youtube newest features",
            "football world cup results",
            "top viewed videos last year",
            "australian open singles results"
        ]
        tree = build_index(pages)
        results = search(tree, "results")
        self.assertEqual(len(results), 3)
        self.assertCountEqual(results, [
            "australian open singles results",
            "football world cup results",
            "hash code competition results are announced"
        ])

    def test_views(self):
        pages = [
            "google code jam is launching",
            "hash code competition results are announced",
            "google launches tech elevate program",
            "code jam final round",
            "youtube newest features",
            "football world cup results",
            "top viewed videos last year",
            "australian open singles results"
        ]
        tree = build_index(pages)
        results = search(tree, "views")
        self.assertEqual(len(results), 0)

    def test_jam_code(self):
        pages = [
            "google code jam is launching",
            "hash code competition results are announced",
            "google launches tech elevate program",
            "code jam final round",
            "youtube newest features",
            "football world cup results",
            "top viewed videos last year",
            "australian open singles results"
        ]
        tree = build_index(pages)
        results = search(tree, "jam code")
        self.assertEqual(len(results), 2)
        self.assertCountEqual(results,[
            "code jam final round",
            "google code jam is launching"
        ])

    def test_google_program(self):
        pages = [
            "google code jam is launching",
            "hash code competition results are announced",
            "google launches tech elevate program",
            "code jam final round",
            "youtube newest features",
            "football world cup results",
            "top viewed videos last year",
            "australian open singles results"
        ]
        tree = build_index(pages)
        results = search(tree, "google program")
        self.assertEqual(len(results), 1)
        self.assertCountEqual(results,[
            "google launches tech elevate program"
        ])


if __name__ == '__main__':
    unittest.main()