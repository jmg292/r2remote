import json

from ._pipe_holder import PipeHolder
from ._base_command_handler import BaseCommandHandler


class GetFunctionList(BaseCommandHandler):

    @staticmethod
    def _get_return_value(response_dict):
        return_value = []
        wanted_keys = ["offset", "name", "minbound", "maxbound"]
        for item in response_dict:
            parsed_item = {}
            for key_name in wanted_keys:
                if key_name in item:
                    parsed_item[key_name] = item[key_name]
            if len(parsed_item) == len(wanted_keys):
                return_value.append(parsed_item)
        return json.dumps(return_value)

    def handle(self, *args):
        response_dict = None
        try:
            pipe = PipeHolder.get_pipe()
            response_dict = pipe.cmd("aflj")
        except ValueError:
            return_value = "Pipe must be opened before analyzing."
        if response_dict is not None:
            try:
                response_dict = json.loads(response_dict)    
                return_value = self._get_return_value(response_dict)            
            except (json.JSONDecodeError, ValueError):
                return_value = "Unable to parse JSON"
        return return_value