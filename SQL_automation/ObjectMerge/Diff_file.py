#!/usr/bin/env python3
""" Command line interface to difflib.py providing diffs in four formats:

* ndiff:    lists every line and highlights interline changes.
* context:  highlights clusters of changes in a before/after format.
* unified:  highlights clusters of changes in an inline format.
* html:     generates side by side comparison with change highlights.

"""

import sys, os, difflib, argparse
from datetime import datetime, timezone
from CustomisedFileOperation import *

def file_mtime(path):
    t = datetime.fromtimestamp(os.stat(path).st_mtime,
                               timezone.utc)
    return t.astimezone().isoformat()

def main():

    parser = argparse.ArgumentParser()
    # parser.add_argument('-c', action='store_true', default=False,
    #                     help='Produce a context format diff (default)')
    # parser.add_argument('-u', action='store_true', default=False,
    #                     help='Produce a unified format diff')
    # parser.add_argument('-m', action='store_true', default=False,
    #                     help='Produce HTML side by side diff '
    #                          '(can use -c and -l in conjunction)')
    # parser.add_argument('-n', action='store_true', default=False,
    #                     help='Produce a ndiff format diff')
    parser.add_argument('-l', '--lines', type=int, default=3,
                        help='Set number of context lines (default 3)')
    parser.add_argument('fromfile')
    parser.add_argument('tofile')
    options = parser.parse_args()

    n = options.lines
    fromfile = options.fromfile
    tofile = options.tofile

    fromdate = file_mtime(fromfile)
    todate = file_mtime(tofile)
    with open(fromfile) as ff:
        fromlines = ff.readlines()
    with open(tofile) as tf:
        tolines = tf.readlines()

    # if options.u:
    #     diff = difflib.unified_diff(fromlines, tolines, fromfile, tofile, fromdate, todate, n=n)
    # elif options.n:
    #     diff = difflib.ndiff(fromlines, tolines)
    # elif options.m:
    #     diff = difflib.HtmlDiff().make_file(fromlines,tolines,fromfile,tofile,context=options.c,numlines=n)
    # else:
    #     diff = difflib.context_diff(fromlines, tolines, fromfile, tofile, fromdate, todate, n=n)
    #
    # # sys.stdout.writelines(diff)
    diff_uni = difflib.unified_diff(fromlines, tolines, fromfile, tofile, fromdate, todate, n=3)
    diff_ndif = difflib.ndiff(fromlines, tolines)
    diff_context = difflib.context_diff(fromlines, tolines, fromfile, tofile, fromdate, todate, n=n)


    write_into_file('diff_uni.sql', contents=''.join(diff_uni), mode='w') # I like because , work is so simple  index
    write_into_file('diff_ndif.sql', contents=''.join(diff_ndif), mode='w') # existing logic ,
    write_into_file('diff_context.sql', contents=''.join(diff_context), mode='w')

    Regex_patters = [
        '-(\d+,\d+)\s+[+](\d+,\d+)' # -1786,67 +1789,29
        ,'-(\d+)\s+[+](\d+)' # -991 +994
        ,'-(\d+,\d+)\s+[+](\d+)' # -813,0 +816
        ,'-(\d+)\s+[+](\d+)' # -70 +70

    ]

if __name__ == '__main__':
    main()


    # Test cases
    '''
    -1786, 67 + 1789, 29
    -991 + 994
    -856, 0 + 859
    -813, 0 + 816
    -70 + 70
    -1 + 1
    '''

