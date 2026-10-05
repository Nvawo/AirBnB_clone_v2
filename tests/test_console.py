#!/usr/bin/python3
"""Tests for the HBNB command interpreter."""

import unittest
from unittest.mock import patch

from console import HBNBCommand
from models import storage
from models.city import City
from models.place import Place
from models.state import State
from models.user import User


class TestCreateWithParameters(unittest.TestCase):
    """Test create command with parameters."""

    def setUp(self):
        """Set up a command interpreter."""
        storage._FileStorage__objects = {}
        self.console = HBNBCommand()

    def test_create_state_with_string(self):
        """Test creating a State with a string parameter."""
        with patch("sys.stdout"):
            self.console.onecmd('create State name="California"')

        states = storage.all(State)
        self.assertEqual(len(states), 1)

        state = list(states.values())[0]
        self.assertEqual(state.name, "California")

    def test_create_city_with_string_parameters(self):
        """Test creating a City with string parameters."""
        with patch("sys.stdout"):
            self.console.onecmd(
                'create City state_id="0001" '
                'name="San_Francisco_is_super_cool"'
            )

        cities = storage.all(City)
        self.assertEqual(len(cities), 1)

        city = list(cities.values())[0]
        self.assertEqual(city.state_id, "0001")
        self.assertEqual(city.name, "San Francisco is super cool")

    def test_create_user_with_parameters(self):
        """Test creating a User with several parameters."""
        with patch("sys.stdout"):
            self.console.onecmd(
                'create User email="test@example.com" '
                'password="1234" first_name="John" last_name="Doe"'
            )

        users = storage.all(User)
        self.assertEqual(len(users), 1)

        user = list(users.values())[0]
        self.assertEqual(user.email, "test@example.com")
        self.assertEqual(user.password, "1234")
        self.assertEqual(user.first_name, "John")
        self.assertEqual(user.last_name, "Doe")

    def test_create_place_with_numbers(self):
        """Test creating a Place with integer and float parameters."""
        with patch("sys.stdout"):
            self.console.onecmd(
                'create Place city_id="0001" user_id="0001" '
                'name="My_little_house" number_rooms=4 '
                'number_bathrooms=2 max_guest=10 price_by_night=300 '
                'latitude=37.773972 longitude=-122.431297'
            )

        places = storage.all(Place)
        self.assertEqual(len(places), 1)

        place = list(places.values())[0]
        self.assertEqual(place.city_id, "0001")
        self.assertEqual(place.user_id, "0001")
        self.assertEqual(place.name, "My little house")
        self.assertEqual(place.number_rooms, 4)
        self.assertEqual(place.number_bathrooms, 2)
        self.assertEqual(place.max_guest, 10)
        self.assertEqual(place.price_by_night, 300)
        self.assertEqual(place.latitude, 37.773972)
        self.assertEqual(place.longitude, -122.431297)

    def test_invalid_parameter_is_ignored(self):
        """Test that an unknown parameter is ignored."""
        with patch("sys.stdout"):
            self.console.onecmd(
                'create State name="California" unknown="value"'
            )

        states = storage.all(State)
        self.assertEqual(len(states), 1)

        state = list(states.values())[0]
        self.assertEqual(state.name, "California")
        self.assertFalse(hasattr(state, "unknown"))


if __name__ == "__main__":
    unittest.main()
