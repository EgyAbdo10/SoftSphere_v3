#!/usr/bin/python3
"""build a file storage engine"""

import json
import os
from dateutil import parser # to parse aware datatime strings

from models.base_model import BaseModel
from models.category import Category
from models.project import Project
from models.users import User
from models.tools import Tool

cls_names = {"BaseModel": BaseModel, "Category": Category,
            "Project": Project, "Tool": Tool, "User": User}

class FileStorage:
    """create file stoarge instances"""

    __objects = {}
    __file_path = "file.json"

    def all(self, cls=None):
        """get all objects in a dict format
        cls: the class itself or its name
        """
        new_dict = {}

        if cls in cls_names.values():
            for key, val in FileStorage.__objects.items():
                if val.__class__ == cls:
                    new_dict[key] = val

        elif cls in cls_names.keys():
            for key, val in FileStorage.__objects.items():
                if val.__class__.__name__ == cls:
                    new_dict[key] = val

        else:
            for key, val in FileStorage.__objects.items():
                new_dict[key] = val

        return new_dict
    
    def new(self, obj):
        """
        add a new object to the __objects dict:
        where the key is
        (class_name of the object + "." + obj.id) | and |value is the obj
        """
        key = obj.__class__.__name__ + "." + str(obj.id)
        FileStorage.__objects[key] = obj

    def save(self):
        """
        itarate over dict items and create a new dict:
        where the keys are the same and the values are
        the dictionary representaion of the objects (using to_dict())
        and then save the newly created dict to the .json file
        """
        new_dict = {}
        for key, val in self.all().items():
            new_dict[key] = val.to_dict()
        with open(FileStorage.__file_path, "w") as f:
            json.dump(new_dict, f)

    def delete(self, obj):
        """delete an object and save changes to the file storage"""
        obj_key = obj.__class__.__name__ + "." + str(obj.id)
        for key in FileStorage.__objects.keys():
            if obj_key == key:
                del FileStorage.__objects[obj_key]
                self.save()
                return True

        return False
    
    def reload(self):
        """reload all data to the __objects public attribute"""
        if os.path.exists(FileStorage.__file_path):
            try:
                with open(FileStorage.__file_path, "r") as f:
                    data_dict = json.load(f)
                    for key, obj_dict in data_dict.items():
                        cls_name = obj_dict["__class__"]
                        del obj_dict["__class__"]
                        # change the datetime string to a datetime aware object
                        obj_dict["created_at"] = parser.isoparse(obj_dict["created_at"])
                        obj_dict["updated_at"] = parser.isoparse(obj_dict["updated_at"])

                        FileStorage.__objects[key] = (
                            cls_names[cls_name](**obj_dict)
                        )
            except:
                pass
        else:
            with open(FileStorage.__file_path, "w") as f:
                """cretae a new file if it doesn't exist"""
                ...

    def find(self, cls_name, id):
        """search anf find objects by id an object"""
        try:
            return self.__objects[f"{cls_name}.{id}"]
        except:
            return None
    
    def filter(self, cls_name, attr, condition, value):
        """filter data based on a condition on only one attribute"""
        conditions = {
            "eq": lambda attr, val: attr == val,
            "gt": lambda attr, val: attr > val,
            "lt": lambda attr, val: attr < val,
            "gte": lambda attr, val: attr >= val,
            "lte": lambda attr, val: attr <= val,
            "ne": lambda attr, val: attr != val,
        }
        if cls_name in cls_names:
            if condition not in conditions:
                return None
            objs = list(self.all(cls_name).values())
            matched_objs = []
            for obj in objs:
                if conditions[condition](getattr(obj, attr, None), value):
                    matched_objs.append(obj)
            return matched_objs
        else:
            return None


    def count(self, cls_name=None):
        """
        count all objects of a class or 
        count all objects from all classes
        """
        count = 0
        if cls_name in cls_names:
            count = len(self.all(cls_name).values())
        else:
            for cls_name in cls_names:
                count += len(self.all(cls_name))
        return count
    
    def close(self):
        """reload data"""
        self.reload()