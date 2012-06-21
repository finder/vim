#!/usr/bin/env python2

import pbs
from pbs import git, ls, cat, grep, test
import json
from cmd2 import Cmd
import sys

def _mkname(name):
    return name[name.rfind('/')+1:].replace('.git', '').replace('.vim', '')

def load(name, path, repos):
    try:
        test('-d', path)
    except pbs.ErrorReturnCode:
        git('submodule', 'add', repos, path)


class ReposManager(Cmd):
    def do_load(self, arg):
        struct = json.load(open('repos.json'))
        for dirname in struct:
            for bundle in struct[dirname]:
                name = _mkname(bundle)
                load(name, dirname + '/' + name, bundle)

    def do_add(self, arg):
        if len(arg) != 2:
            print "Required arguments are (repos, dirname)"
            sys.exit(-1)
        repos, dirname = arg

        with open('repos.json') as f:
            struct = json.load(f)
            bundles = struct.setdefault(dirname, [])
            if repos not in bundles:
                bundles.append(repos)

        with open('repos.json', 'w') as f:
            json.dump(struct, f)

    def do_update(self, arg):
        git('submodule foreach git submodule update'.split(' '))

if __name__ == '__main__':
    app = ReposManager()
    app.cmdloop()
