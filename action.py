#! /usr/bin/env python
# -*- coding: UTF-8 -*-

import alp
from initdb import save_list
import sys

if __name__ == '__main__':
    args = sys.argv[1:]
    if (len(args) < 1):
        alp.feedback([])
    elif (args[0] == '>'):
        if (args[1] == 'init'):
            initdb.save_list() # notif?
