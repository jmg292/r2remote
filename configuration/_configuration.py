import json

from .exceptions import InvalidConfigurationError


class Configuration(object):

    def __init__(self):
        self.enabled_plugins = []
        self.identity_file_path = ""
        self.authorized_keys_folder = ""
        self.bind_addr = "0.0.0.0"
        self.bind_port = 40960
        self.socket_timeout = 5

    @property
    def filesystem_paths(self):
        return ["identity_file_path", "authorized_keys_folder"]

    def to_string(self):
        return json.dumps(self.__dict__, indent=4)

    def save_to_file(self, output_file):
        with open(output_file, "w") as outfile:
            outfile.write(self.to_string())

    @staticmethod
    def from_dict(config_dict):
        config_object = Configuration()
        required_config_elements = config_object.__dict__
        for key in required_config_elements:
            if key not in config_dict:
                raise InvalidConfigurationError(f"Key not found: {key}")
        for key in config_dict:
            if not hasattr(config_object, key):
                raise InvalidConfigurationError(f"Unknown configuration element: {key}")
            setattr(config_object, key, config_dict[key])
        return config_object

    @staticmethod
    def from_string(config_string):
        config_dict = json.loads(config_string)
        return Configuration.from_dict(config_dict)

    @staticmethod
    def from_file(config_file):
        with open(config_file, "r") as infile:
            config_string = infile.read()
        return Configuration.from_string(config_string)
