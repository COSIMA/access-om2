
import sys
import os
import tempfile
import tarfile
import hashlib
import argparse

def calc_checksum(dirname):
    """
    Calculate the checksum of a whole directory.

    This is done but tarring the directory first to make sure that file names
    and other metadata are included in the checksum.

    FIXME: this doesn't work, subsequent invokations of the function do not
    give the same value. This may be because the tmp file name is different
    each time.
    """

    _, tmp = tempfile.mkstemp(suffix='.tar')
    with tarfile.open(tmp, "w") as tar:
        tar.add(dirname)

    h = hashlib.md5()

    with open(tmp, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            h.update(chunk)

    # Delete tarball now that hash has been calculated.
    os.remove(tmp)

    return h.hexdigest()[:8]


def main():

    parser = argparse.ArgumentParser()
    parser.add_argument('dirpath', help='Path of directory whose checksum to return.')

    args = parser.parse_args()

    checksum = calc_checksum(args.dirpath)
    print(checksum)


if __name__ == '__main__':
    sys.exit(main())
