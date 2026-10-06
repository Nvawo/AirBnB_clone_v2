#!/usr/bin/python3
"""Tests for the console"""
import os
import unittest
from io import StringIO
from unittest.mock import patch
from console import HBNBCommand
from models import storage
from models.state import State

DB = os.getenv('HBNB_TYPE_STORAGE') == 'db'


class TestConsole(unittest.TestCase):
    """Tests HBNBCommand"""

    def run_cmd(self, cmd):
        """Run a console command and return its output"""
        with patch('sys.stdout', new=StringIO()) as out:
            HBNBCommand().onecmd(cmd)
            return out.getvalue().strip()

    def remove_state(self, state_id):
        """Delete a State created by a test"""
        obj = storage.all(State).get("State." + state_id)
        if obj is not None:
            storage.delete(obj)
            storage.save()

    def test_quit(self):
        """quit returns True"""
        self.assertTrue(HBNBCommand().onecmd("quit"))

    def test_EOF(self):
        """EOF returns True"""
        self.assertTrue(HBNBCommand().onecmd("EOF"))

    def test_emptyline(self):
        """Empty line prints nothing"""
        self.assertEqual(self.run_cmd(""), "")

    def test_create_missing_class(self):
        """create with no class"""
        self.assertEqual(self.run_cmd("create"), "** class name missing **")

    def test_create_bad_class(self):
        """create with unknown class"""
        self.assertEqual(self.run_cmd("create MyModel"),
                         "** class doesn't exist **")

    def test_show_missing_class(self):
        """show with no class"""
        self.assertEqual(self.run_cmd("show"), "** class name missing **")

    def test_show_bad_class(self):
        """show with unknown class"""
        self.assertEqual(self.run_cmd("show MyModel 1"),
                         "** class doesn't exist **")

    def test_destroy_missing_class(self):
        """destroy with no class"""
        self.assertEqual(self.run_cmd("destroy"), "** class name missing **")

    @unittest.skipIf(DB, "FileStorage only")
    def test_create_state_filestorage(self):
        """create State prints an id and adds an object"""
        before = len(storage.all(State))
        state_id = self.run_cmd('create State name="California"')
        self.assertEqual(len(state_id), 36)
        self.assertEqual(len(storage.all(State)), before + 1)
        self.remove_state(state_id)

    @unittest.skipIf(DB, "FileStorage only")
    def test_create_state_name_filestorage(self):
        """create State stores the name parameter"""
        state_id = self.run_cmd('create State name="New_York"')
        obj = storage.all(State)["State." + state_id]
        self.assertEqual(obj.name, "New York")
        self.remove_state(state_id)

    @unittest.skipIf(not DB, "DBStorage only")
    def test_create_state_prints_id_db(self):
        """create State prints an id under DBStorage"""
        state_id = self.run_cmd('create State name="California"')
        self.assertEqual(len(state_id), 36)
        self.remove_state(state_id)


if __name__ == '__main__':
    unittest.main()
