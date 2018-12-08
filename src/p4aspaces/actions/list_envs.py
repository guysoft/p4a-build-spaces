
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

