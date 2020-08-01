import json
import os
import string

from ._base_command_handler import BaseCommandHandler


class ListVolumes(BaseCommandHandler):

    def handle(self, *args):
        available_drives = ["/"]
        if "nt" in os.name:
            available_drives = [f"{letter}:\\" for letter in string.ascii_uppercase if os.path.exists(f"{letter}:")]
        return_value = []
        for drive_letter in available_drives:
            return_value.append({
                "name": drive_letter,
                "path": drive_letter,
                "item_type": "DIRECTORY",
                "mime_type": "inode/directory"
            })
        return json.dumps(return_value)


class ListDirectory(BaseCommandHandler):

    def handle(self, *args):
        return_value = "Usage: list_directory [directory_path]"
        if len(args):
            folder_path = os.path.abspath(args[0])
            if os.path.isdir(folder_path):
                contained_items = []
                try:
                    fs_items = os.listdir(folder_path)                
                    for fs_item in fs_items:
                        item_dict = {
                            "name": fs_item,
                            "path": os.path.join(folder_path, fs_item),
                            "item_type": "UNKNOWN",
                            "mime_type": "UNKNOWN"
                        }
                        if os.path.isfile(item_dict["path"]):
                            item_dict["item_type"] = "FILE"
                        elif os.path.isdir(item_dict["path"]):
                            item_dict["item_type"] = "DIRECTORY"
                            item_dict["mime_type"] = "inode/directory"
                        contained_items.append(item_dict)
                except (OSError, PermissionError) as e:
                    contained_items.append({
                        "name": str(e),
                        "path": folder_path,
                        "item_type": "ERROR",
                        "mime_type": "ERROR"
                    })
                return_value = json.dumps(contained_items)
            else:
                return_value = f"Invalid directory: {folder_path}"
        return return_value
