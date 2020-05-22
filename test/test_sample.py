import unittest
from pathlib import Path

from anisub.__main__ import main

SAMPLE_PATH = r'C:\path\to\sample.mkv'


class MainTest(unittest.TestCase):

    def test_main(self):
        main(input_path=Path(SAMPLE_PATH))


if __name__ == '__main__':
    unittest.main()
