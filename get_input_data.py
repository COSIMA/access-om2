#!/usr/bin/env python

import sys
import os, errno
import shlex
import shutil
import subprocess as sp
import argparse

data_filename = 'input_154112e8.tar.gz'

data_path = '/short/public/access-om2/' + data_filename
data_url = 'http://s3-ap-southeast-2.amazonaws.com/dp-drop/access-om2/' + data_filename

def main():

    my_dir = os.path.dirname(os.path.realpath(__file__))
    tarball = os.path.join(my_dir, data_filename)

    if os.path.exists('input'):
        return 0

    # Download input data.
    if not os.path.exists(data_filename):
        if not os.path.exists(data_path):
            sp.check_call(['wget', '-P', my_dir, data_url])
        else:
            shutil.copy(data_path, my_dir)

    sp.check_call(['tar', 'zxvf', tarball, '-C', my_dir])

    return 0

if __name__ == '__main__':
    sys.exit(main())
