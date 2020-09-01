import json


class InfoClass(object):

    def load_dict(self, info_dict):
        wanted_keys = list(self.__dict__.keys())
        for key in wanted_keys:
            if key in info_dict:
                setattr(self, key, info_dict[key])

    @staticmethod
    def from_dict(class_instance, info_dict):
        class_instance.load_dict(info_dict)
        return class_instance


class CoreInfo(InfoClass):

    def __init__(self):
        self.type = ""
        self.file = ""
        self.fd = 0
        self.size = 0
        self.humansz = ""
        self.iorw = False
        self.mode = ""
        self.obsz = ""
        self.block = 0
        self.format = ""


class BinaryInfo(InfoClass):

    def __init__(self):
        self.arch = ""
        self.binsz = 0
        self.bintype = ""
        self.bits = 0
        self.canary = False
        self.bin_class = ""
        self.compiled = ""
        self.crypto = ""
        self.dbg_file = ""
        self.endian = ""
        self.havecode = False
        self.guid = ""
        self.intrp = ""
        self.lang = ""
        self.linenum = False
        self.lsyms = False
        self.machine = ""
        self.maxopsz = 0
        self.minopsz = 0
        self.nx = False
        self.os = ""
        self.pic = False
        self.pcalign = 0
        self.relocs = False
        self.relro = ""
        self.rpath = ""
        self.static = False
        self.stripped = False
        self.subsys = ""
        self.va = False

    def load_dict(self, binary_info_dict):
        super().load_dict(binary_info_dict)
        if "class" in binary_info_dict:
            self.bin_class = binary_info_dict["class"]


class FileInfo(InfoClass):

    def __init__(self):
        self.binary = BinaryInfo()
        self.core = CoreInfo()

    @property
    def __dict__(self):
        file_info = {}
        file_info_keys = ["binary", "core"]
        for info_type in file_info_keys:
            data_dict = getattr(self, info_type).__dict__
            for key_name in data_dict.keys():
                file_info[f"{info_type}_{key_name}"] = data_dict[key_name]
        return file_info

    def __str__(self):
        return json.dumps(self.__dict__)

    def load_dict(self, file_info_dict):
        if "bin" in file_info_dict:
            self.binary.load_dict(file_info_dict["bin"])
        if "core" in file_info_dict:
            self.core.load_dict(file_info_dict["core"])

    @staticmethod
    def from_string(file_info_string):
        return_value = FileInfo()
        return_value.load_dict(json.loads(file_info_string))
        return return_value


class StringInfo(InfoClass):

    def __init__(self):
        self.vaddr = 0
        self.paddr = 0
        self.ordinal = 0
        self.size = 0
        self.length = 0
        self.section = ""
        self.type = ""
        self.data = ""    

    def load_dict(self, string_info):
        if "string" in string_info:
            string_info["data"] = string_info["string"]
            del string_info["string"]
        super().load_dict(string_info)

    @staticmethod
    def from_dict(string_dict):
        return InfoClass.from_dict(StringInfo(), string_dict)

    @staticmethod
    def load_all_strings(string_info):
        string_dict = json.loads(string_info)
        return [StringInfo.from_dict(x) for x in string_dict["strings"]]

    