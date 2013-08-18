#!/usr/bin/env python

import sys
import robot
import argparse


def build_arg_parser():
    parser = argparse.ArgumentParser(description='Suite helper')
    parser.add_argument('-s', '--suite',
            default='suites',
            help='The suite to test')
    parser.add_argument('-n', '--name',
            default='*',
            help='The name of the test case to execute')
    return parser

def main(args):
    # Parse all the arguments
    parser = build_arg_parser()
    args = parser.parse_args(args)

    # Run the specified robot test
    robot.run(args.suite, test=args.name)


if __name__ == '__main__':
    main(sys.argv[1:])
