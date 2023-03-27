import shlex
import cmd
import socket
import readline
import threading


receiving = True


def parse(args):
    return shlex.split(args, comments=True)


def request(req):
    global COWsocket
    COWsocket.send(f"{req}\n".encode())


def receive(cmdline):
    global receiving, COWsocket
    while receiving:
        msg = COWsocket.recv(1024).decode()
        if msg.strip() == "exit":
            break

        print(f"\n{msg.strip()}\n{cmdline.prompt}{readline.get_line_buffer()}", end="", flush=True)


class COW(cmd.Cmd):
    intro = "<<< Welcome to cowchat >>>"
    prompt = "(COW) "

    def do_login(self, args):
        match parse(args):
            case [nickname, ]:
                request(f"login {nickname}")
            case _:
                print("There should be one argument")

    def do_who(self, args):
        request("who")

    def do_cows(self, args):
        request("cows")

    def do_say(self, args):
        match parse(args):
            case [cow, text, ]:
                request(f"say {cow} {text}")
            case _:
                print("There should be two arguments")

    def do_yield(self, args):
        match parse(args):
            case [text, ]:
                request(f"yield {text}")
            case _:
                print("There should be one argument")

    def do_quit(self, args):
        global recieving
        request("quit")
        recieving = False
        return True


with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as COWsocket:
    COWsocket.connect(("localhost", 1337))
    cmdline = COW()
    receiver = threading.Thread(target=receive, args=(cmdline,))
    receiver.start()
    cmdline.cmdloop()
