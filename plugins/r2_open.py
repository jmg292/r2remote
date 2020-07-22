import os

from ._pipe_holder import PipeHolder
from ._base_command_handler import BaseCommandHandler


class Open(BaseCommandHandler):

    def handle(self, *args):
        return_value = "Usage: open [file_path]"
        if len(args):
            file_path = os.path.abspath(args[0])
            pipe = PipeHolder.get_pipe(file_path)
            pipe.cmd("aaa")
            return_value = f"{file_path} opened and analyzed."
        return return_value