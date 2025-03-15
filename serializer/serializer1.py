import json
from typing import Any, Self, Dict, List, Set, Callable, Type, TypeVar, get_args, get_origin

class Serializable:
    def serialize(self) -> Any:
        pass

    def deserialize(json_obj: Any) -> Self:
        pass

class Test(Serializable):
    t: str

    def serialize(self) -> Any:
        return str
    
    def deserialize(json_obj) -> Self:
        if isinstance(json_obj, str):
            t = Test()
            t.t = json_obj
            return t
        raise Exception("Error deserializing chunk pos, json_obj is not a str")

class ChunkPos(Serializable):
    x: int
    y: int

    def __init__(self, x: int, y: int) -> None:
        self.x = x
        self.y = y

    def serialize(self) -> Any:
        return f"{self.x},{self.y}"
    
    def deserialize(json_obj) -> Self:
        if isinstance(json_obj, str):
            pos = json_obj.split(",")
            x = int(pos[0])
            y = int(pos[1])
            return ChunkPos(x, y)
        raise Exception("Error deserializing chunk pos, json_obj is not a str")

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

    def __init__(self, x: int, y: int, t: Test, c: list[ChunkPos], d: dict[int, int], e: dict[str, int]):
        self.x = x
        self.y = y
        self.t = t
        self.c = c
        self.d = d
        self.e = e

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

def transform_load(_type: Type[Any], obj: Any, transform_func: Callable[[Type[Serializable], Serializable], Any]) -> Any:
    if get_origin(_type) is list:
        new_list = []
        inner_type = get_args(_type)[0]
        for item in obj:
            new_list.append(transform_load(inner_type, item, transform_func))
        return new_list
    elif _type is Dict:
        new_dict = {}
        inner_type_0 = get_args(_type)[0]
        inner_type_1 = get_args(_type)[1]
        for (key, val) in obj.items():
            new_dict[transform_load(inner_type_0, key, transform_func)] = transform_load(inner_type_1, val, transform_func)
        return new_dict
    elif isinstance(_type, Type) and issubclass(_type, Serializable):
        return transform_func(_type, obj)
    return obj

T = TypeVar('T')

def deserialize(_type: Type[T], json_obj: dict[Any, Any]) -> T:
    if hasattr(_type, "__annotations__"):
        new_dict = {}
        for (key, val) in json_obj.items():
            if key in _type.__annotations__.keys():
                new_val = val
                new_dict[key] = transform_load(_type.__annotations__[key], new_val, lambda type, obj: type.deserialize(obj))
        return _type(**new_dict)
    else:
        raise Exception("Can only deserialize class with type hints")
    
def main():
    json_obj = load_json("serializer/test.json")
    obj = deserialize(MyClass, json_obj)
    print(f"{obj.t.t}")

if __name__ == "__main__":
    main()
