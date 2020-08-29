import os

from ._pipe_holder import PipeHolder
from ._base_command_handler import BaseCommandHandler


class Open(BaseCommandHandler):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        global _r2_opened
        _r2_opened = False

    def handle(self, *args):
        global _r2_opened
        return_value = "Usage: open [file_path]"
        if len(args):
            file_path = os.path.abspath(args[0])
            pipe = PipeHolder.get_pipe(file_path)
            pipe.cmd("aaa; aab; aac; aaf")
            _r2_opened = True
            return_value = f"{file_path} opened and analyzed."
        return return_value


def on_unload():
    global _r2_opened
    if _r2_opened:
        PipeHolder.close_pipe()
        _r2_opened = False
        print("[+] r2pipe closed.")