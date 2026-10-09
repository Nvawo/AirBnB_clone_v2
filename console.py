#!/usr/bin/python3
"""Contains the entry point of the command interpreter."""
import cmd
import re
import shlex

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
        "Place": Place,
        "State": State,
        "City": City,
        "Amenity": Amenity,
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

    def _parse_create_arguments(self, args):
        """Parse create command parameters."""
        lexer = shlex.shlex(args, posix=False)
        lexer.whitespace_split = True
        lexer.commenters = ""

        try:
            parts = list(lexer)
        except ValueError:
            return []

        if not parts:
            return []

        class_name = parts[0]

        if class_name not in HBNBCommand.classes:
            return parts

        model = HBNBCommand.classes[class_name]
        valid_keys = set()

        if hasattr(model, "__table__"):
            valid_keys = {
                column.name for column in model.__table__.columns
            }

        if class_name == "Place":
            valid_keys.add("amenity_ids")

        parsed = [class_name]

        for parameter in parts[1:]:
            if "=" not in parameter:
                continue

            key, value = parameter.split("=", 1)

            if key not in valid_keys:
                continue

            if not value:
                continue

            if value.startswith('"') and value.endswith('"'):
                value = value[1:-1]
                value = value.replace('\\"', '"')
                value = value.replace("_", " ")
                parsed.append((key, value))
                continue

            if re.fullmatch(r"[-+]?\d+", value):
                parsed.append((key, int(value)))
                continue

            if re.fullmatch(
                r"[-+]?(?:\d+\.\d*|\.\d+)",
                value
            ):
                parsed.append((key, float(value)))
                continue

        return parsed

    def do_create(self, args):
        """Create an object: create <Class> <key=value> ..."""
        if not args:
            print("** class name missing **")
            return
        parts = args.split()
        if parts[0] not in HBNBCommand.classes:
            print("** class doesn't exist **")
            return
        kwargs = {}
        for param in parts[1:]:
            if "=" not in param:
                continue
            key, value = param.split("=", 1)
            if len(value) >= 2 and value[0] == '"' and value[-1] == '"':
                value = value[1:-1].replace('\\"', '"').replace("_", " ")
            else:
                try:
                    value = int(value)
                except ValueError:
                    try:
                        value = float(value)
                    except ValueError:
                        continue
            kwargs[key] = value
        try:
            instance = HBNBCommand.classes[parts[0]](**kwargs)
            instance.save()
            print(instance.id)
        except Exception:
            return

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

        return line


if __name__ == "__main__":
    HBNBCommand().cmdloop()
