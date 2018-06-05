#!/usr/bin/env python

import sys
import os
import errno
import shlex
import shutil
import subprocess as sp
import argparse

data_filename = 'input_4fd9d93e.tar.gz'

data_path = '/short/public/access-om2/' + data_filename
furl = 'http://s3-ap-southeast-2.amazonaws.com/dp-drop/access-om2/%s'
data_url = furl % data_filename


def main():

    my_dir = os.path.dirname(os.path.realpath(__file__))
    tarball = os.path.join(my_dir, data_filename)

    # POTENTIAL BUG: assumes 'input' was produced from data_filename - TODO: also check timestamp?
    if os.path.exists('input') and os.path.exists(data_filename):
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
