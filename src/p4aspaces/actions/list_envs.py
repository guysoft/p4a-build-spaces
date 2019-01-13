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
import sys

from p4aspaces.actions import actions
import p4aspaces.buildenv as buildenv

def list_envs(args):
    argparser = argparse.ArgumentParser(
        description="action \"list-envs\": " +
        str(actions()["list-envs"]["description"]))
    args = argparser.parse_args(args)

    # List environments:
    envs = buildenv.get_environments()
    print("Available environments:")
    for env in envs:
        print("  " + env.name + "\n     " + env.description)
    print("")
    print("Launch shell with:\n" +
        "  p4aspaces shell " +
        sorted([env.name for env in envs])[0])
    sys.exit(0)

