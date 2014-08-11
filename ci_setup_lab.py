#!/usr/bin/env python

import sys
import os, errno
import shutil
import shlex
import subprocess as sp

"""
Set up the payu lab and input directories before running tests. 
"""

def mkdir_p(path):
    try:
        os.makedirs(path)
    except OSError as exc: # Python >2.5
        if exc.errno == errno.EEXIST and os.path.isdir(path):
            pass
        else: raise


def clone(repo_url, dest):

    # Clone the experiments directory. 
    path = os.path.join(dest, '.git')
    if not os.path.exists(path):
        cmd = 'git clone {} {}'.format(repo_url, dest)
        sp.check_call(shlex.split(cmd))

    curdir = os.getcwd()
    os.chdir(dest)
    sp.check_call(shlex.split('git checkout master'))
    sp.check_call(shlex.split('git pull'))
    os.chdir(curdir)


def main():

    clone('https://github.com/nicholash/payu-experiments.git',
          'payu-experiments')

    mkdir_p('lab/archive')
    mkdir_p('lab/bin')
    mkdir_p('lab/codebase')

    if not os.path.exists('lab/input'):
        os.symlink('/short/v45/nah599/access/input', 'lab/input')
    shutil.copy('/short/v45/nah599/access/bin/um7.3x', 'lab/bin')

if __name__ == '__main__':
    sys.exit(main())
