from .handler import CommandHandler
from configuration import Configuration


class CommandHandlerFactory(object):

    _instance = None

    @staticmethod
    def get_instance(config: Configuration) -> CommandHandler:
        if CommandHandlerFactory._instance is None:
            new_instance = CommandHandler(config)
            # Allow support for dirty monkey patching
            if CommandHandlerFactory._instance is None:
                CommandHandlerFactory._instance = new_instance
        return CommandHandlerFactory._instance
