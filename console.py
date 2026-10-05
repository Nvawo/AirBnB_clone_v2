#!/usr/bin/python3
"""Contains the entry point of the command interpreter."""
import cmd
import re

from models import storage
from models.base_model import BaseModel
from models.user import User
from models.state import State
from models.city import City
from models.amenity import Amenity
from models.place import Place
from models.review import Review


class HBNBCommand(cmd.Cmd):
    """Command interpreter for the AirBnB project."""

    prompt = "(hbnb) "

    classes = {
        "BaseModel": BaseModel,
        "User": User,
        "State": State,
        "City": City,
        "Amenity": Amenity,
        "Place": Place,
        "Review": Review
    }

    def do_quit(self, args):
        """Quit command to exit the program."""
        return True

    def do_EOF(self, args):
        """Exit the program when EOF is received."""
        print()
        return True

    def emptyline(self):
        """Do nothing when an empty line is entered."""
        pass

    def do_create(self, args):
        """Create an object of any class."""
        if not args:
            print("** class name missing **")
            return

        if args not in HBNBCommand.classes:
            print("** class doesn't exist **")
            return

        new_instance = HBNBCommand.classes[args]()
        storage.new(new_instance)
        storage.save()
        print(new_instance.id)

    def do_show(self, args):
        """Print the string representation of an instance."""
        if not args:
            print("** class name missing **")
            return

        parts = args.split()

        if parts[0] not in HBNBCommand.classes:
            print("** class doesn't exist **")
            return

        if len(parts) < 2:
            print("** instance id missing **")
            return

        key = "{}.{}".format(parts[0], parts[1])
        obj = storage.all().get(key)

        if obj is None:
            print("** no instance found **")
            return

        print(obj)

    def do_destroy(self, args):
        """Delete an instance based on the class name and id."""
        if not args:
            print("** class name missing **")
            return

        parts = args.split()

        if parts[0] not in HBNBCommand.classes:
            print("** class doesn't exist **")
            return

        if len(parts) < 2:
            print("** instance id missing **")
            return

        key = "{}.{}".format(parts[0], parts[1])
        obj = storage.all().get(key)

        if obj is None:
            print("** no instance found **")
            return

        storage.delete(obj)
        storage.save()

    def do_all(self, args):
        """Print all string representations of instances."""
        if args:
            parts = args.split()

            if parts[0] not in HBNBCommand.classes:
                print("** class doesn't exist **")
                return

            objects = storage.all(HBNBCommand.classes[parts[0]])
        else:
            objects = storage.all()

        print([
            str(obj) for obj in objects.values()
        ])

    def do_count(self, args):
        """Count the number of instances of a class."""
        if not args:
            print("** class name missing **")
            return

        parts = args.split()

        if parts[0] not in HBNBCommand.classes:
            print("** class doesn't exist **")
            return

        objects = storage.all(HBNBCommand.classes[parts[0]])
        print(len(objects))

    def do_update(self, args):
        """Update an instance based on the class name and id."""
        if not args:
            print("** class name missing **")
            return

        parts = args.split()

        if parts[0] not in HBNBCommand.classes:
            print("** class doesn't exist **")
            return

        if len(parts) < 2:
            print("** instance id missing **")
            return

        key = "{}.{}".format(parts[0], parts[1])
        obj = storage.all().get(key)

        if obj is None:
            print("** no instance found **")
            return

        if len(parts) < 3:
            print("** attribute name missing **")
            return

        if len(parts) < 4:
            print("** value missing **")
            return

        attr_name = parts[2]
        attr_value = parts[3]

        if attr_name in ["id", "created_at", "updated_at"]:
            return

        try:
            attr_value = eval(attr_value)
        except (NameError, SyntaxError):
            pass

        setattr(obj, attr_name, attr_value)
        storage.save()

    def precmd(self, line):
        """Parse advanced command syntax."""
        match = re.match(
            r"^(\w+)\.(\w+)\((.*)\)$",
            line
        )

        if match:
            class_name = match.group(1)
            command = match.group(2)
            arguments = match.group(3)

            if command == "all":
                return "all {}".format(class_name)

            if command == "count":
                return "count {}".format(class_name)

            if command == "show":
                match_id = re.search(
                    r'id=["\']?([^,"\']+)["\']?',
                    arguments
                )
                if match_id:
                    return "show {} {}".format(
                        class_name,
                        match_id.group(1)
                    )

            if command == "destroy":
                match_id = re.search(
                    r'id=["\']?([^,"\']+)["\']?',
                    arguments
                )
                if match_id:
                    return "destroy {} {}".format(
                        class_name,
                        match_id.group(1)
                    )

            if command == "update":
                match_id = re.search(
                    r'id=["\']?([^,"\']+)["\']?',
                    arguments
                )
                match_dict = re.search(
                    r"\{(.*)\}",
                    arguments
                )

                if match_id and match_dict:
                    instance_id = match_id.group(1)
                    dictionary = match_dict.group(1)

                    pairs = re.findall(
                        r'["\']([^"\']+)["\']\s*:\s*'
                        r'(["\'].*?["\']|[^,]+)',
                        dictionary
                    )

                    if pairs:
                        commands = []

                        for attribute, value in pairs:
                            value = value.strip()
                            commands.append(
                                "update {} {} {} {}".format(
                                    class_name,
                                    instance_id,
                                    attribute,
                                    value
                                )
                            )

                        return ";".join(commands)

        return line


if __name__ == "__main__":
    HBNBCommand().cmdloop()
