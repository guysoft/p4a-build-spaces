
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
        print(" " + env.name + "\n     " + env.description)
    sys.exit(0)

