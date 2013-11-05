import alp
import sys
from initdb import save_list
from subprocess import Popen

def do_cmd(cmd):
    pass # TODO

def go_url(u):
    Popen(['osascript', '-e', 'open location "%s"' % u])

def main():
    if len(sys.argv) < 2:
        return

    typ, arg = sys.argv[1].split(':', 1)

    if typ == 'cmd':
        return do_cmd(arg)
    elif typ == 'url':
        return go_url(arg)

if __name__ == '__main__':
    main()
