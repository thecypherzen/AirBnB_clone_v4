#!/usr/bin/python3
"""
This is a program that contains the entry point of the command interpreter
"""
import ast
import cmd
from models.amenity import Amenity
from models.base_model import BaseModel
from models import storage
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State
from models.user import User
from os import system
import re


class HBNBCommand(cmd.Cmd):
    """ This is a class that defines the command interpreter """
    prompt = "(hbnb) "
    __classes = {"Amenity": Amenity, "BaseModel": BaseModel, "City": City,
                 "Place": Place, "Review": Review, "State": State,
                 "User": User}

    def do_quit(self, line):
        """ Quit command to exit the program """
        return True

    def do_EOF(self, line):
        """ EOF command to exit the program """
        print()
        return True

    def emptyline(self):
        """
            This function is called when the user\
            passes and emptyline to the console
        """
        pass

    def do_create(self, line):
        """
            Creates a new instance of BaseModel and
            saves it (to the JSON file) and prints the id.
            Ex: $ create BaseModel
        """
        if line == "":
            print("** class name missing **")
        elif line not in self.__classes:
            print("** class doesn't exist **")
        else:
            new_obj = self.__classes[line]()
            new_obj.save()
            print(new_obj.id)

    def do_show(self, line):
        """
            Prints the string representation of an instance
            based on the class name and id.
            Ex: $ show BaseModel 1234-1234-1234
        """
        input_args = line.split(" ")
        if self._validate(input_args):
            instance = self._get_instance(input_args[1], input_args[0])
            if instance:
                print(instance)

    def do_destroy(self, line):
        """ Deletes an instance based on the class name and id
            (save the change into the JSON file)
            Ex: $ destroy BaseModel 1234-1234-1234
        """
        input_args = line.split()
        if self._validate(input_args):
            instance = self._get_instance(input_args[1], input_args[0])
            if instance:
                storage.destroy(instance)
                storage.save()

    def do_all(self, model_name):
        """
            Prints all string representation of all instance\
            based or not on the class name.
            Ex: $ all BaseModel or $ all
        """
        if model_name:
            if model_name not in self.__classes:
                print("** class doesn't exist **")
                return
            else:
                all_models = storage.all(model_name)
        else:
            all_models = storage.all()
        models_list = [str(model) for model in all_models.values()]
        print(models_list)

    def do_update(self, line):
        """
            Updates an instance based on the class name and id by
            adding or updating attribute, and save the change into the
            JSON file).
            Ex: $ update BaseModel 1234-1234-1234 email 'aibnb@mail.com
        """
        input_args = line.split()
        if not self._validate(input_args):
            return
        input_len = len(input_args)
        if input_len < 4:
            if input_len == 2:
                print("** attribute name missing **")
            else:
                print("** value missing **")
            return
        instance = self._get_instance(input_args[1], input_args[0])
        if input_args[2] not in ["id", "created_at", "updated_at"]:
            if input_args[3][0] == input_args[3][-1] == '"':
                value = input_args[3][1:-1]
            else:
                value = input_args[3]
            setattr(instance, input_args[2], value)
            instance.save()

    def do_clear(self, line):
        """ Clears the screen of the console """
        system('clear')

    def _validate(self, input_args):
        """checks if class_name exists and obj_id are passed"""
        arg_len = len(input_args)
        if arg_len == 0:
            print("** class name missing **")
        elif input_args[0] not in self.__classes:
            print("** class doesn't exist **")
        elif arg_len == 1:
            print("** instance id missing **")
        else:
            return True
        return False

    def _get_instance(self, obj_id, obj_name=None):
        instance = None
        all_objs = storage.all(obj_name).values()
        for obj in all_objs:
            if obj.id == obj_id:
                instance = obj
                break
        if not instance:
            print("** no instance found **")
        return instance

    def _pop_next_arg(self, args_list):
        """Pops out the next arg from last args_list element"""
        next_args = args_list[-1].split(",", maxsplit=1)
        new_args = [arg for arg in args_list[:-1]]
        next_args[0] = next_args[0].strip()
        return new_args + next_args

    def default(self, line):
        """Handles default commands

        First checks if a valid method is called on a Class,
          e.g. BaseModel.all()
          - if so, it handles it or prints a default message
        """
        # check if line matches pattern: Class.method()
        regex = r'^[A-Za-z]+\.[a-z]+\(.*\)$'
        match = re.search(regex, line)
        resolved = True
        if match:
            # get Class and check if exists
            input = line.split('.', maxsplit=1)
            if input[0] not in self.__classes:
                print("** class doesn't exist **")
                return
            # get values from rest of cmd and handle
            regex = '[)(]'
            input = [input[0]] + [val for val in
                                  re.split(regex, input[1]) if val]
            i_len = len(input)
            if input[1] == "all" and i_len == 2:
                self.do_all(input[0])
            elif input[1] == "count" and i_len == 2:
                print(len(storage.all(input[0]).values()))
            elif input[1] not in ["all", "count"]:
                input = self._pop_next_arg(input)
                i_len = len(input)
                if i_len < 3:
                    print("** instance id missing **")
                    return
                if input[1] not in ["show", "destroy", "update"]:
                    print(f"*** Unknown syntax: {line}")
                    return
                instance = self._get_instance(input[2], input[0])
                if instance:
                    if input[1] == "show" and i_len == 3:
                        print(instance)
                    elif input[1] == "destroy" and i_len == 3:
                        storage.destroy(instance)
                        storage.save()
                    elif input[1] == "update":
                        if i_len == 3:
                            print("** attribute name missing **")
                            return
                        # handle values passed as dict
                        input[-1] = input[-1].strip()
                        if input[-1][0] == "{" and input[-1][-1] == "}":
                            value = ast.literal_eval(input[-1])
                            for key, val in value.items():
                                setattr(instance, key, val)
                                instance.save()
                            return
                        # handle values passed normally
                        input = self._pop_next_arg(input)
                        i_len = len(input)
                        if i_len == 4:
                            print("** value missing **")
                            return
                        input[4] = input[4].strip()
                        try:
                            num = int(input[4])
                            setattr(instance, input[3], num)
                        except ValueError:
                            try:
                                num = float(input[4])
                                setattr(instance, input[3], num)
                            except ValueError:
                                setattr(instance, input[3], input[4])
                                instance.save()
                    else:
                        resolved = False
            else:
                resolved = False
        if not resolved:
            print(f"*** Unknown syntax: {line}")


if __name__ == '__main__':
    HBNBCommand().cmdloop()
