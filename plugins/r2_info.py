import json

from ._info_classes import FileInfo, StringInfo
from ._pipe_holder import PipeHolder
from ._base_command_handler import BaseCommandHandler


class GetBinaryInfo(BaseCommandHandler):

    def handle(self, *args):
        file_info_json = None
        try:
            pipe = PipeHolder.get_pipe()
            file_info_json = pipe.cmd("ij")
        except ValueError:
            return_value = "Pipe must be opened before analyzing."
        if file_info_json:
            try:
                return_value = str(FileInfo.from_string(file_info_json))
            except (ValueError, json.JSONDecodeError):
                return_value = "Unable to decode JSON"
        return return_value


class GetEntrypoints(BaseCommandHandler):

    def handle(self, *args):
        try:
            pipe = PipeHolder.get_pipe()
            return_value = pipe.cmd("iej")
        except ValueError:
            return_value = "Pipe must be opened before analyzing."
        return return_value


class GetMainAddress(BaseCommandHandler):

    def handle(self, *args):
        try:
            pipe = PipeHolder.get_pipe()
            return_value = pipe.cmd("iMj")
        except ValueError:
            return_value = "Pipe must be opened before analyzing."
        return return_value


class GetStrings(BaseCommandHandler):

    def handle(self, *args):
        string_data = None
        try:
            pipe = PipeHolder.get_pipe()
            string_data = pipe.cmd("izzj")
        except ValueError:
            return_value = "Pipe must be opened before analyzing."
        if string_data is not None:
            return_value = json.dumps([x.__dict__ for x in StringInfo.load_all_strings(string_data)])
        return return_value


class GetExports(BaseCommandHandler):

    def handle(self, *args):
        try:
            pipe = PipeHolder.get_pipe()
            return_value = pipe.cmd("iEj")
        except ValueError:
            return_value = "Pipe must be opened before analyzing."
        return return_value


class GetSymbols(BaseCommandHandler):

    def handle(self, *args):
        try:
            pipe = PipeHolder.get_pipe()
            return_value = pipe.cmd("isj")
        except ValueError:
            return_value = "Pipe must be opened before analyzing."
        return return_value


class GetImports(BaseCommandHandler):

    def handle(self, *args):
        try:
            pipe = PipeHolder.get_pipe()
            return_value = pipe.cmd("iij")
        except ValueError:
            return_value = "Pipe must be opened before analyzing."
        return return_value


class GetRelocations(BaseCommandHandler):

    def handle(self, *args):
        try:
            pipe = PipeHolder.get_pipe()
            return_value = pipe.cmd("irj").strip()
            if return_value:
                unpacked_json = json.loads(return_value)
                return_value = []
                for value in unpacked_json:
                    if value["name"] is None:
                        value["name"] = ""
                    return_value.append(value)
                return_value = json.dumps(return_value)
        except ValueError:
            return_value = "Pipe must be opened before analyzing."
        return return_value