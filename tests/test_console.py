import unittest
from unittest.mock import patch, MagicMock
from io import StringIO
from console import HBNBCommand

class TestHBNBCommand(unittest.TestCase):

    @patch('sys.stdout', new_callable=StringIO)
    def test_help_quit(self, mock_stdout):
        console = HBNBCommand()
        console.onecmd("help_quit")
        self.assertEqual(mock_stdout.getvalue(), "Exits the program with formatting\n\n")

    def test_do_quit(self):
        console = HBNBCommand()
        with self.assertRaises(SystemExit):
            console.onecmd("quit")

    @patch('sys.stdout', new_callable=StringIO)
    def test_create(self, mock_stdout):
        console = HBNBCommand()
        console.oncecmd('create BaseModel name=test_model')

if __name__ == "__main__":
    unittest.main()

