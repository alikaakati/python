from xmlrpc.client import ServerProxy, Fault
from cmd import Cmd
from random import choice
from string import ascii_lowercase
from server import Node, UNHANDLED
from threading import Thread
from time import sleep
import sys
HEAD_START = 0.1 # Seconds
SECRET_LENGTH = 100


def random_string(length):
    chars = []
    letters = ascii_lowercase[:26]
    while length > 0:
        length -= 1
        chars.append(choice(letters))
    return ''.join(chars)


class Client(Cmd):
    prompt = '> '
    def __init__(self, url, dirname, urlfile):
        Cmd.__init__(self)
        self.secret = random_string(SECRET_LENGTH)
        print(urlfile)
        n = Node(url, dirname, self.secret)
        t = Thread(target=n._start) 
        t.setDaemon(1)
        t.start()
        # Give the server a head start:
        sleep(HEAD_START)
        print("server : " , url)
        self.server = ServerProxy(url)
        for line in open(urlfile):
            print('reading line')
            line = line.strip()
            print(line)
            self.server.hello(line)
    def do_fetch(self, arg):
        try:
            self.server.fetch(arg, self.secret)
            print('working')
        except Fault as f:
            if f.faultCode != UNHANDLED: raise
            print("Couldn't find the file", arg)
    def do_exit(self, arg):
        print()
        sys.exit()
    do_EOF = do_exit


def main():
    urlfile, directory, url = sys.argv[1:]
    client = Client(url, directory, urlfile)
    client.cmdloop()
if __name__ == '__main__': main()
