import atexit
import r2pipe


class PipeHolder(object):

    _pipe_instance = None

    @staticmethod
    def close_pipe():
        if PipeHolder._pipe_instance is not None:
            PipeHolder._pipe_instance.quit()

    @staticmethod
    def get_pipe(file_path = "") -> r2pipe.open_base.OpenBase:
        if PipeHolder._pipe_instance is None:
            if not file_path:
                raise ValueError("File path must be supplied at object creation.")
            PipeHolder._pipe_instance = r2pipe.open(file_path)
        return PipeHolder._pipe_instance