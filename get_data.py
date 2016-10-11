#!/usr/bin/env python

import sys
import os, errno
import shlex
import subprocess as sp
import argparse

def main():

    # Download input data.
    data = '/short/public/access-om/access-om.tar.gz'

    cmd = '/bin/tar -zxvf {}'.format(data)
    ret = sp.call(shlex.split(cmd))
    return ret


if __name__ == '__main__':
    sys.exit(main())
