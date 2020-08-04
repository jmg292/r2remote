import argparse
import base64
import io
import json
import socket

from message_wrapper import MessageWrapper
from protocol import Message, MessageHandlerMixin


class ShellHandler(MessageHandlerMixin):

    def __init__(self, identity_key, authorized_hosts, secure = True):
        self.message_wrapper = MessageWrapper(identity_key, authorized_hosts)
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.rfile = io.BytesIO()  # Here, hold this for a moment
        self.secure = secure

    def _do_handshake(self):
        print(f"[+] Authenticating . . .")
        challenge = base64.b64decode(self.rfile.readline().strip())
        print(f"[+] Got challenge: {challenge}")
        self._write_line(self.message_wrapper.get_challenge_response(challenge))
        server_response = base64.b64decode(self.rfile.readline().strip())
        print(f"[+] Got response: {server_response}")
        self.message_wrapper.finalize_handshake(server_response)
        print("[+] Authentication successful!")

    def connect(self, remote_addr, remote_port):
        self.socket.connect((remote_addr, remote_port))
        self.rfile = self.socket.makefile()
        if self.secure:
            self._do_handshake()
        else:
            print("[+] Insecure flag is set, skipping authentication")

    def run(self):
        command = ""
        while command != "exit":
            command = input("> ").lower().strip()
            if command:
                for packed_message in Message.packed_from_string(self.message_wrapper, command, secure=self.secure):
                    self._write_line(packed_message)
                if command != "exit":                    
                    response = self._get_message(self.message_wrapper, secure=self.secure)
                    try:
                        # Try to pretty print JSON responses
                        response = json.loads(response)                        
                        response = json.dumps(response, indent=4)
                    except (ValueError, json.JSONDecodeError):
                        pass
                    print(response)


if __name__ == "__main__":
    argument_parser = argparse.ArgumentParser(description="Connect a terminal to an r2remote session.")
    argument_parser.add_argument("--identity-key", "-i", required=True, help="Path to identity file.")
    argument_parser.add_argument("--authorized-hosts", "-a", required=True, help="Path to authorized hosts directory.")
    argument_parser.add_argument("--host", required=True, help="IP address to connect to.")
    argument_parser.add_argument("--port", "-p", required=True, type=int, help="Port to connect to.")
    argument_parser.add_argument("--insecure", help="Disable authentication and encryption (Probably shouldn't ever use this.)", required=False, default=False, action="store_true")


    arguments = argument_parser.parse_args()
    print("[+] Initializing . . . ", end='')
    shell = ShellHandler(arguments.identity_key, arguments.authorized_hosts, not arguments.insecure)
    print("Done.\n[+] Connecting . . . ")
    shell.connect(arguments.host, arguments.port)
    print("[+] Starting shell.")
    shell.run()
