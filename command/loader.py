import importlib
import inspect
import os
import pkgutil
import re

from plugins._base_command_handler import BaseCommandHandler


class CommandLoader(object):

    def __init__(self, authorized_commands, config):
        self.config = config
        self._case_conversion_pattern = re.compile(r'(?<!^)(?=[A-Z])')
        self._command_list = authorized_commands

    def _resolve_commands_in_module(self, module):
        loaded_commands = {}
        for name, loaded_class in inspect.getmembers(module, inspect.isclass):
            if name != "BaseCommandHandler":
                try:                
                    if BaseCommandHandler in inspect.getmro(loaded_class):
                        command_name = self._case_conversion_pattern.sub("_", name).lower()
                        loaded_commands[command_name] = loaded_class(self.config)
                except AttributeError:
                    continue
        return loaded_commands

    def load_commands(self, plugin_folder, bypass_load_functions=False):
        loaded_commands = {
            "_on_unload": []
        }
        for _, module_name, _ in pkgutil.iter_modules([plugin_folder]):
            # Skip modules and packages starting with _
            if not module_name.startswith("_"):
                # Load only authorized commands
                if module_name in self._command_list:
                    # Load the module into memory
                    loaded_module = importlib.import_module(f'plugins.{module_name}')
                    # Handle load and unload hooks
                    if hasattr(loaded_module, "on_load") and not bypass_load_functions:
                        loaded_module.on_load()
                    if hasattr(loaded_module, "on_unload"):
                        loaded_commands["_on_unload"].append(loaded_module.on_unload)
                        print(f"[+] Registerd unload hook for {module_name}")
                    else:
                        print(f"[+] No unload hooks found for {module_name}")
                    loaded_commands = {**loaded_commands, **self._resolve_commands_in_module(loaded_module)}
        return loaded_commands
