#!/usr/bin/env python2

import os
import sys
from argparse import ArgumentParser
from scantron import ScantronGenerator, inch

# Make this file easier to use by adding nice arguments
parser = ArgumentParser(description='Generate scantron PDFs.')
parser.add_argument(
        '-o', '--output',
        action='store', default='form.pdf',
        metavar='FILE',
        help='Filename to use for generated scantrons. Defaults to forms.pdf.')
parser.add_argument(
        '-n', '--num-matches',
        action='store', default=1,
        metavar='NUMBER', type=int,
        help='Number of matches to generate sheets for. Defaults to 1.')
parser.add_argument(
        'data',
        metavar='input_data',
        help='File where the field data is stored. ' +
                'This must be a python script with an array called "data" ' +
                'of Field entries.')
parser.add_argument(
        '--collate',
        choices=['on', 'off'],
        default='on',
        help='Turns collatating on or off. Default is on.')

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

# If everything went well, proceed to generate the PDF
st = ScantronGenerator(args.output, spacing=0.3*inch)
st.set_box_sizes(box_size=0.2*inch, box_spacing=0.3*inch)
st.populate(data, matches=args.num_matches, collate=args.collate)
st.save()
