#!/usr/bin/python3
"""
Contains the TestDBStorageDocs classes
"""

import unittest
import models
from models.engine import db_storage
DBStorage = db_storage.DBStorage


class TestDBStorage(unittest.TestCase):
    """Test the DBStorage class"""

    def test_all_returns_dict(self):
        """Test that all returns a dictionary"""
        self.assertIsInstance(models.storage.all(), dict)


if __name__ == "__main__":
    unittest.main()
