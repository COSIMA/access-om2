#!/usr/bin/env python

import sys
import os, errno
import shlex
import sh
import subprocess as sp
import argparse

data_filename = 'input_b8053e87.tar.gz'

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
            sh.wget('-P', my_dir, data_url)
        else:
            sh.cp(data_path, my_dir)

    sh.tar('zxvf', tarball, '-C', my_dir)

    return 0

if __name__ == '__main__':
    sys.exit(main())
