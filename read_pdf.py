#!/usr/bin/env python2

import os
import sys
from argparse import ArgumentParser
from scantron import ScantronParser

# Make this file easier to use by adding nice arguments
parser = ArgumentParser(description='Parse scanned scantron sheets.')
parser.add_argument(
        'data',
        metavar='input_data',
        help='File where the field data is stored. ' +
                'This must be a python script with an array called "data" ' +
                'of Field entries.')

args = parser.parse_args()

# If the file has a .py extension, we should still accept it
if args.data.endswith('.py'):
    args.data = os.path.splitext(args.data)[0]

# Import the file specified on the command line
try:
    __import__(args.data)
    data = sys.modules[args.data].data
except ImportError:
    print('Failed to import %s.' % args.data)
    quit(1)
except AttributeError:
    print('Could not find data array.')
    quit(1)

# If everything went well, proceed to parse the filled scantron
st = ScantronParser()
st.scan(data, 'pages/page-1.jpg')
