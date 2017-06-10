#!/usr/bin/env python

import sys
import os, errno
import shlex
import sh
import subprocess as sp
import argparse

data_path = '/short/public/access-om2/input_6912b015.tar.gz'
data_url = 'http://s3-ap-southeast-2.amazonaws.com/dp-drop/access-om2/input_6912b015.tar.gz'

def main():

    my_dir = os.path.dirname(os.path.realpath(__file__))
    tarball = os.path.join(my_dir, 'input_6912b015.tar.gz')

    # Download input data.
    if not os.path.exists(data_path):
        sh.wget('-P', my_dir, data_url)
    else:
        sh.cp(data_path, my_dir)

    sh.tar('zxvf', tarball, '-C', my_dir)

    return 0

if __name__ == '__main__':
    sys.exit(main())
