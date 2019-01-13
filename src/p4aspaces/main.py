#!/usr/bin/python3

'''
Copyright (c) 2018-2019 p4a-build-spaces team and others, see AUTHORS.md

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
THE SOFTWARE.
'''

import argparse
import os
import shutil
import subprocess
import sys
import tempfile
import uuid
import urllib.parse

from p4aspaces.actions import actions

def main(args=None):
    if args is None:
        args = sys.argv[1:]
    argparser = argparse.ArgumentParser()
    argparser.add_argument("action",
        nargs=1,
        help="The p4a-build-spaces action out of \"" +
        "\", \"".join(sorted([aname for aname in actions().keys()])) +
        "\"",
        )
    argparser.add_argument("arguments",
        nargs=argparse.REMAINDER,
        help="The arguments to the action. Use " +
        "\"p4aspaces <action> --help\" to see available " +
        "arguments and options for an action, e.g. " +
        "\"p4aspaces shell --help\"")

    if len(args) == 0:
        argparser.print_help(sys.stderr)
        print("p4aspaces: error: the following argument " +
            "is required: action", file=sys.stderr, flush=True)
        sys.exit(1)
    args = argparser.parse_args(args)
    if len(args.action) > 0:
        args.action = args.action[0]
    if args.action not in actions().keys():
        print("p4aspaces: error: not a known action: \"" + str(args.action) +
            "\".", file=sys.stderr, flush=True)
        print("       Available actions are:",
            file=sys.stderr, flush=True)
        print("        - " + "\n        - ".join(actions().keys()),
            file=sys.stderr, flush=True)
        print("       Get more detailed help on an action like this:",
            file=sys.stderr, flush=True)
        print("          p4aspaces " +
            str(list(actions().keys())[0]) + " --help",
            file=sys.stderr, flush=True)
        sys.exit(1)
    actions()[args.action]["function"](args.arguments)

if __name__ == "__main__":
    main(sys.argv[1:])

