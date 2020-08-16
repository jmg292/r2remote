import os

from .loader import CommandLoader


class CommandHandler(object):

    def __init__(self, config):
        self.config = config
        self._internal_commands = ["help", "?"]
        self._available_commands = CommandLoader(config.enabled_plugins, config).load_commands(
            os.path.join(config.base_directory, "plugins")
        )

    def _handle_internal_commands(self, command, *args):
        return_value = "Invalid command."
        if command == "help" or command == "?":
            return_value = f"Available commands: {', '.join(self.supported_commands)}"
        return return_value

    @property
    def supported_commands(self):
        return self._internal_commands + list(self._available_commands.keys())

    def can_handle_command(self, command):
        return command.lower() in self.supported_commands

    def handle_command(self, command, *args):
        command = command.lower()
        response = "Invalid command."
        if self.can_handle_command(command):
            if command in self._internal_commands:
                response = self._handle_internal_commands(command, *args)
            else:
                response = self._available_commands[command].handle(*args)
        return response

    def unload_all(self):
        for unload_hook in self._available_commands["_on_unload"]:
            unload_hook()