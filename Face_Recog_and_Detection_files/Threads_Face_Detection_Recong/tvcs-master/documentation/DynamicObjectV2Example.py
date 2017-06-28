#!/usr/bin/python

# import from parent directory
import sys
import os.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir)))

import DynamicObjectV2
Obj = DynamicObjectV2.Class

# create object
print("# create object:")
obj = Obj("a", 5, "b", "something")
print(obj)
print("")

# access with dot notation
print("# access with dot notation")
print(obj.a)
print("")

# update / create field with dot notation
print("# update / create field with dot notation")
obj.c = True
print(obj)
print("")

# access like a dictionary / map
print("# access like a dictionary / map")
print(obj["a"])
print("")

# update / create field like a dictionary / map
print("# update / create field like a dictionary / map")
obj["d"] = 8
print(obj)
print("")

# extend object with dictionary - only affects values specified
print("# update object - only affects values specified")
obj.extend("a", 10, "e", False)
print(obj)
print("")

# extend object with another Obj
print("# extend object with another Obj")
obj2 = Obj("a", 999, "w", True)
obj.extend(obj2)
print(obj)
print("")

# nested objects
print("# nested objects")
obj.f = Obj("x", 1, "y", 2, "z", 3)
print(obj)
print("")


# another way of nesting objects
print("# another way of nesting objects")
obj3 = Obj(
    'x', 1,
    'a', 3,
    'z', Obj(
             'z01', 1,
             'z02', 3,
             'z03', 6,
             'z04', True
         ),
    'f', True
)
print(obj3)
print("")