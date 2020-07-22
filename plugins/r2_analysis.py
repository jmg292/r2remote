from ._pipe_holder import PipeHolder
from ._base_command_handler import BaseCommandHandler


class GetEntrypoint(BaseCommandHandler):


    def handle(self, *args):
        try:
            pipe = PipeHolder.get_pipe()
            return_value = pipe.cmd("iej")
        except ValueError:
            return_value = "Pipe must be opened before analyzing."
        return return_value


class GetFunctionList(BaseCommandHandler):

    def handle(self, *args):
        try:
            pipe = PipeHolder.get_pipe()
            return_value = pipe.cmd("aflj")
        except ValueError:
            return_value = "Pipe must be opened before analyzing"
        return return_value