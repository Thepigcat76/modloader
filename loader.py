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
        return f"ModConfig{{id: \"{self.id}\", name: \"{self.name}\", version: {self.version}, description: \"{self.description}\"}}"

from serializer.serializer1 import *
import importlib
import sys
import os
import context

def run_function_from_file(module_name: str, function_name: str, file_path: str):
    # Generate a unique module name
    unique_module_name = f"{module_name}_{os.path.basename(os.path.dirname(file_path))}"

    # Load module dynamically
    spec = importlib.util.spec_from_file_location(unique_module_name, file_path)
    if spec is None or spec.loader is None:
        raise ImportError(f"Could not load module from {file_path}")

    module = importlib.util.module_from_spec(spec)
    sys.modules[unique_module_name] = module  # Add to sys.modules to prevent GC
    spec.loader.exec_module(module)  # Execute the module

    # Get the function and execute it
    function = getattr(module, function_name)
    function(context.ModContext("Deez"))

def main():
    with os.scandir("mods") as entries:
        for entry in entries:
            name = entry.name
            if entry.is_dir() and not name.startswith("_"):
                json_obj = load_json(f"mods/{name}/mod.json")
                config = deserialize(ModConfig, json_obj)
                print(config)
                run_function_from_file("mod", "init", f"mods/{name}/src/mod.py")

if __name__ == "__main__":
    main()
