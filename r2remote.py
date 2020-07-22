import argparse
import base64
import os
import socket
import socketserver

from message_wrapper import MessageWrapper
from configuration import Configuration
from command import CommandHandlerFactory
from protocol import Message, MessageHandlerMixin


configuration = Configuration()


class MessageHandler(socketserver.StreamRequestHandler, MessageHandlerMixin):

    def _write_line(self, message: bytes):
        self.wfile.write(base64.b64encode(message) + b"\n")
        self.wfile.flush()    

    def command_loop(self, message_wrapper):
        command_handler = CommandHandlerFactory.get_instance(configuration)
        while True:
            split_message = self._get_message(message_wrapper).split()
            command = split_message[:1][0].lower()
            args = split_message[1:]
            if command == "exit":
                return
            elif command_handler.can_handle_command(command):
                response = command_handler.handle_command(command, *args)
            else:
                response = "Invalid command."
            for packed_message in Message.packed_from_string(message_wrapper, response):
                self._write_line(packed_message)

    def handle(self):
        print("[+] Client connected!")
        message_wrapper = MessageWrapper(configuration.identity_file_path, configuration.authorized_keys_folder)
        original_timeout = self.server.socket.timeout
        self.server.socket.settimeout(configuration.socket_timeout)
        self.socket = self.server.socket
        try:
            print("[+] Sending handshake challenge . . .")
            self._write_line(message_wrapper.get_challenge())
            challenge_response = base64.b64decode(self.rfile.readline().strip())
            # This will throw a permission error if client authorization fails.  Not ideal, but I can't reset the handshake yet, so this is the behavior I want for now
            print("[+] Validating client response . . .")
            server_response = message_wrapper.finalize_handshake(challenge_response)
            print(f"[+] Successful authentication from client at {self.client_address[0]}")
            self._write_line(server_response)            
        finally:
            self.server.socket.settimeout(original_timeout)
        self.command_loop(message_wrapper)
        print("[+] Session terminated.")


def resolve_path(base_directory, path):
    if not os.path.isabs(path):
        abs_path = os.path.abspath(path)
        if not os.path.exists(abs_path):
            abs_path = os.path.join(base_directory, path)
        path = abs_path
    return path


def resolve_absolute_paths(base_directory):
    for filesystem_path in configuration.filesystem_paths:
        path = resolve_path(base_directory, getattr(configuration, filesystem_path, ""))
        if not os.path.exists(path):
            raise OSError(f"Could not find configured {filesystem_path} element at {path}.  Please check your configuration file.")
        setattr(configuration, filesystem_path, path)


if __name__ == "__main__":
    base_directory = os.path.realpath(os.path.dirname(__file__))

    argument_parser = argparse.ArgumentParser(description="Networked remote control for radare2")
    config_group = argument_parser.add_argument_group("Configuration")
    config_group.add_argument("--config-file", "-c", help="Path to configuration file", required=False, default=os.path.join(base_directory, "config.json"))
    config_group.add_argument("--generate-config", "-gc", help="Generate a new, empty configuration file and exit.", required=False, action="store_true")

    arguments = argument_parser.parse_args()

    config_path = resolve_path(base_directory, arguments.config_file)

    if not arguments.generate_config:
        configuration = Configuration.from_file(config_path)
        resolve_absolute_paths(base_directory)
        setattr(configuration, "base_directory", base_directory)        
        print(f"[+] Starting server on {configuration.bind_addr}:{configuration.bind_port}")
        with socketserver.TCPServer((configuration.bind_addr, configuration.bind_port), MessageHandler) as tcp_server:
            tcp_server.serve_forever()
    else:
        configuration.save_to_file(config_path)
