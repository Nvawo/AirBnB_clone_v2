#!/usr/bin/python3
"""Tests for DBStorage (uses MySQLdb to check the real database)"""
import os
import unittest
from io import StringIO
from unittest.mock import patch

DB = os.getenv('HBNB_TYPE_STORAGE') == 'db'

if DB:
    import MySQLdb
    from console import HBNBCommand
    from models import storage
    from models.state import State


def count_rows(table):
    """Count rows in a table with a fresh MySQLdb connection"""
    conn = MySQLdb.connect(
        host=os.getenv('HBNB_MYSQL_HOST', 'localhost'),
        user=os.getenv('HBNB_MYSQL_USER'),
        passwd=os.getenv('HBNB_MYSQL_PWD'),
        db=os.getenv('HBNB_MYSQL_DB'))
    cur = conn.cursor()
    cur.execute("SELECT COUNT(*) FROM {}".format(table))
    total = cur.fetchone()[0]
    cur.close()
    conn.close()
    return total


@unittest.skipIf(not DB, "DBStorage tests only run with db storage")
class TestDBStorage(unittest.TestCase):
    """Tests DBStorage"""

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

    def test_all_returns_dict(self):
        """all() returns a dict"""
        self.assertIsInstance(storage.all(), dict)

    def test_all_with_class_returns_dict(self):
        """all(State) returns a dict"""
        self.assertIsInstance(storage.all(State), dict)

    def test_all_class_filter(self):
        """all(State) only holds State objects"""
        state = State(name="Filter")
        storage.new(state)
        storage.save()
        for obj in storage.all(State).values():
            self.assertIsInstance(obj, State)
        self.remove_state(state.id)

    def test_console_create_state_adds_row(self):
        """create State name="California" adds exactly one row"""
        before = count_rows("states")
        state_id = self.run_cmd('create State name="California"')
        after = count_rows("states")
        self.assertEqual(after - before, 1)
        self.remove_state(state_id)

    def test_console_create_two_states(self):
        """Two create commands add two rows"""
        before = count_rows("states")
        first = self.run_cmd('create State name="Texas"')
        second = self.run_cmd('create State name="Nevada"')
        after = count_rows("states")
        self.assertEqual(after - before, 2)
        self.remove_state(first)
        self.remove_state(second)

    def test_new_save_adds_row(self):
        """new + save adds a row"""
        before = count_rows("states")
        state = State(name="Oregon")
        storage.new(state)
        storage.save()
        self.assertEqual(count_rows("states") - before, 1)
        self.remove_state(state.id)

    def test_delete_removes_row(self):
        """delete + save removes the row"""
        state = State(name="Utah")
        storage.new(state)
        storage.save()
        before = count_rows("states")
        storage.delete(state)
        storage.save()
        self.assertEqual(before - count_rows("states"), 1)

    def test_delete_none_does_nothing(self):
        """delete(None) does not change the table"""
        before = count_rows("states")
        storage.delete(None)
        storage.save()
        self.assertEqual(count_rows("states"), before)


if __name__ == '__main__':
    unittest.main()
