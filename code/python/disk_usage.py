#!/usr/bin/env python
# coding=utf-8

import os
import sys
from argparse import ArgumentParser
from pprint import pprint
import operator
import datetime


def convert_bytes(bytes):
    bytes = float(bytes)
    if bytes >= 1099511627776:
        terabytes = bytes / 1099511627776
        size = '%.2fT' % terabytes
    elif bytes >= 1073741824:
        gigabytes = bytes / 1073741824
        size = '%.2fG' % gigabytes
    elif bytes >= 1048576:
        megabytes = bytes / 1048576
        size = '%.2fM' % megabytes
    elif bytes >= 1024:
        kilobytes = bytes / 1024
        size = '%.2fK' % kilobytes
    else:
        size = '%.2fb' % bytes
    return size


def getFileSizes(path):
    """
    @param path: Path to recurse through
    @return: dictionary of { path : { file : size }}
    """
    return {os.path.join(curdir, file): os.stat(os.path.join(curdir, file)).st_size
            for curdir, subdir, files in os.walk(path)
            for file in files
            if os.path.exists(os.path.join(curdir, file)) and not curdir.startswith('/proc')
               and not curdir.startswith('/dev') and os.stat(os.path.join(curdir, file)).st_size
    }


def main(argv):
    start_time = datetime.datetime.now()
    parser = ArgumentParser()
    parser.add_argument('--number', '-n', default='10', help='Number of entries to show')
    parser.add_argument('--outfile', '-o', action='store_true', default=False, dest='out',
                        help='File to output full listing of files')
    parser.add_argument('paths', help='Directory to list size of.')
    args = parser.parse_args()

    out_file = 'disk-usage.json'
    files_dict = {}
    paths_to_do = args.paths
    with open(out_file, 'w') as out_file_handle:
        for path_to_do in paths_to_do:
            for curdir, subdir, files in os.walk(path_to_do):
                for file in files:
                    if os.path.exists(os.path.join(curdir, file)):
                        files_dict[os.path.join(curdir, file)] = os.stat(os.path.join(curdir, file)).st_size
                        out_file_handle.write(
                            '%s,%s\n' % (os.path.join(curdir, file), os.stat(os.path.join(curdir, file)).st_size))

    sorted_files = (sorted(files_dict.iteritems(), key=operator.itemgetter(1), reverse=True))
    nice_numbers = [(file, convert_bytes(bytes)) for file, bytes in sorted_files]

    end_time = datetime.datetime.now()
    delta_time = end_time - start_time

    print delta_time
    if args.number == 'all':
        pprint(nice_numbers)
    else:
        pprint(nice_numbers[:int(args.number)])


if __name__ == '__main__':
    main(sys.argv[1:])
