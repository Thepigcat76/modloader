"""
class AddRepr:
    def __init__(self, cls):
        self.cls = cls
        cls.__repr__ = lambda self: f"{self.__class__.__name__}({self.__dict__})"

    def __call__(self, *args, **kwargs):
        return self.cls(*args, **kwargs)

@AddRepr
class Person:
    def __init__(self, name, age):
        self.name = name
        self.age = age

p = Person("Bob", 25)
print(p)  # Output: Person({'name': 'Bob', 'age': 25})

from typing import Type, Any, Self

class Serializer:
    def serialize(self) -> Any:
        ...
    
    def deserialize() -> Self:
        ...

mappp: dict[type, Serializer] =  {}

class Serializable:
    cls: Type[Any]

    def __init__(self, cls: Type[Any]):
        self.cls = cls.__dict__

@Serializable
"""

import json
from typing import Any, Dict, List, Set, Callable

class Serializable:
    def serialize(self) -> Any:
        pass

    def deserialize(self, json_obj: Any):
        pass

class Test:
    t: str

class ChunkPos(Serializable):
    x: int
    y: int

    def __init__(self, x: int, y: int) -> None:
        self.x = x
        self.y = y

    def serialize(self) -> Any:
        return f"{self.x},{self.y}"

    def __eq__(self, other: Any) -> bool:
        if isinstance(other, MyClass):
            return self.x == other.x and self.y == other.y
        return False

    def __hash__(self) -> int:
        return hash((self.x, self.y))  # Hashing a tuple of x and y

class MyClass:
    x: int
    y: int
    t: Test
    c: list[ChunkPos]
    d: dict[int, int]
    e: dict[str, int]

    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y
        self.t = "Abc"
        self.c = [ChunkPos(10, 20), ChunkPos(320, 10)]
        self.d = {19: 200, 340: 0}
        self.e = {"eeee": 10, "nc": 69}

def load_json(path: str) -> Any:
    with open(path, "r") as file:
        return json.load(file)

def save_json(path: str, json_obj):
    with open(path, "w") as file:
        json.dump(json_obj, file, indent=4) 

def transform(obj: Any, transform_func: Callable[[Serializable], Any]) -> Any:
    if isinstance(obj, List):
        new_list = []
        for item in obj:
            new_list.append(transform(item, transform_func))
        return new_list
    elif isinstance(obj, Dict):
        print(f"dict: {obj}")
        new_dict = {}
        for (key, val) in obj.items():
            print(f"k: {key}, v: {val}")
            new_dict[transform(key, transform_func)] = transform(val, transform_func)
        return new_dict
    elif isinstance(obj, Serializable):
        return transform_func(obj)
    return obj

def transform_save(dict: dict[Any, Any]) -> dict[Any, Any]:
    return transform(dict, lambda obj: obj.serialize())

def deserialize():
    pass

def main():
    #obj = MyClass(100, 200)
    #json_obj = transform_save(pos.__dict__)
    #print(json_obj)
    #save_json("test.json", json_obj)

    json_obj = load_json("test.json")
    obj = deserialize(MyClass, json_obj)
    print(dict)

if __name__ == "__main__":
    main()
