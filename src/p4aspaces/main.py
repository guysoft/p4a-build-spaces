#!/usr/bin/python3

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
        "arguments and options for an action.")

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
        sys.exit(1)
    actions()[args.action]["function"](args.arguments)

if __name__ == "__main__":
    main(sys.argv[1:])

