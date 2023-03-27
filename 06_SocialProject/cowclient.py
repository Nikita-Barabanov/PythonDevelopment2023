import cowsay
import shlex
import cmd
import socket
import readline
import threading
import sys


def parse(args):
    return shlex.split(args, comments=True)


def request(req):
    global COWsocket
    COWsocket.send(f"{req}\n".encode())


def recieve(cmdline):
    global recieving, COWsocket
    while recieving:
        msg = COWsocket.recv(1024).decode()
        if msg.strip() == "exit":
            break

        print(f"\n{msg.strip()}\n{cmdline.prompt}{readline.get_line_buffer()}", end="", flush=True)


class COW(cmd.Cmd):
    intro = "<<< Welcome to cowchat >>>"
    prompt = "(COW) "


with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as COWsocket:
    COWsocket.connect(("localhost", 1337))
    cmdline = COW()
    reciever = threading.Thread(target=recieve, args=(cmdline,))
    reciever.start()
    cmdline.cmdloop()
