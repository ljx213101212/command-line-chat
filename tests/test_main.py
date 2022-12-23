import sys
import unittest
from io import StringIO
from src.main import main


class TestMain(unittest.TestCase):
    def setUp(self):
        self.held, sys.stdout = sys.stdout, StringIO()

    def test_main_should_print_hello_wolrd(self):
        main()
        self.assertEqual(sys.stdout.getvalue(), 'Hello World!\n')
