import alp
from alp import Item
from sys import argv as sys_argv
from initdb import get_list

def cmd_arg(a):
    return 'cmd:' + a

def cmd_title(c):
    return 'pp > ' + c

def main():
    cmds = {
        'init': 'initialize the DB'
    }

    argv = sys_argv
    argc = len(argv)
    items = []

    if argc > 1:
        argv = argv[:1] + argv[1].split()
        argc = len(argv)

    if argv[1] == '>':
        if argc > 2:
            for c in alp.fuzzy_search(argv[2], cmds.keys()):
                t = cmd_title(c)
                i = Item(title=t, autocomplete='> '+c, \
                            subtitle=cmds[c], valid=True, arg=cmd_arg(c))
                items.append(i)
        else:
            for c, st in cmds.iteritems():
                t = cmd_title(c)
                i = Item(title=t, autocomplete='> '+c, \
                            subtitle=st, valid=True, arg=cmd_arg(c))
                items.append(i)
        alp.feedback(items)
        return

    li = get_list()

    ppl = alp.fuzzy_search(' '.join(argv[1:]), li, lambda x: x['name'])

    for p in ppl:
        i = Item(title=p['name'], subtitle='', \
                icon=p['icon'], fileIcon=True, \
                autocomplete=p['name'], valid=True, arg='url:'+p['url'])
        items.append(i)

    alp.feedback(items)

if __name__ == '__main__':
    main()
