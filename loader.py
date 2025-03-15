class ModConfig:
    id: str
    name: str
    version: float
    description: str

    def __init__(self, id, name, version, description):
        self.id = id
        self.name = name
        self.version = version
        self.description = description

    def __str__(self):
        return f"ModConfig{{id: {self.id}, name: {self.name}, version: {self.version}, description: \"{self.description}\"}}"

from serializer.serializer1 import *
import importlib
import sys
import os

def run_function_from_file(module_name: str, function_name: str, file_path: str):
    # Add the directory containing the file to sys.path
    sys.path.append(os.path.dirname(file_path))
    
    # Import the module dynamically
    module = importlib.import_module(module_name)
    
    # Get the function from the module
    function = getattr(module, function_name)
    
    # Call the function
    function()

def main():
    json_obj = load_json("testmod/mod.json")
    config = deserialize(ModConfig, json_obj)
    print(config)
    run_function_from_file("./testmod/src/mod.py", "mod", "init")

if __name__ == "__main__":
    main()
