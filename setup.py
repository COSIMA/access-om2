#!/usr/bin/env python

import sys
import os, errno
import shlex
import subprocess as sp
import argparse

"""
Setup script. Initialises:
    - the payu lab (which includes work, archive and source code directories.)
    - standard experiments.
    - standard model input.
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

    parser = argparse.ArgumentParser()
    parser.add_argument("--download_input_data", default=False, help="""
                        Download experiment input data.""")

    args = parser.parse_args()

    # Download experiments from the Climate and Weather Science Laboratory
    # (cwslab.nci.org.au)
    clone('https://github.com/CWSL/payu-experiments.git', 'experiments')

    mkdir_p('lab/archive')
    mkdir_p('lab/bin')
    mkdir_p('lab/codebase')

    # Download input data.
    data = '/short/public/access-om/access-om.tar.gz'
    if args.download_input_data:
        # FIXME: download from Ramadda.
        # data = ''
        pass

    if not os.path.exists('lab/input'):
        cwd = os.getcwd()
        try:
            os.chdir('lab')
            cmd = '/bin/tar -zxvf {}'.format(data)
            ret = sp.call(shlex.split(cmd))
        finally:
            os.chdir(cwd)

        assert(ret == 0)

    return 0

if __name__ == '__main__':
    sys.exit(main())
