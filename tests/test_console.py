#!/usr/bin/python3
"""
Contains the TestConsoleDocs class
"""

import unittest
import console
HBNBCommand = console.HBNBCommand


class TestHBNBCommand(unittest.TestCase):
    """Test the HBNBCommand class"""

    def test_prompt(self):
        """Test console prompt"""
        self.assertEqual("(hbnb) ", HBNBCommand.prompt)

    def test_emptyline(self):
        """Test emptyline behavior"""
        self.assertFalse(HBNBCommand().emptyline())


if __name__ == "__main__":
    unittest.main()
