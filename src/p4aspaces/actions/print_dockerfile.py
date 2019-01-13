
import argparse
import sys

from p4aspaces.actions import actions
import p4aspaces.buildenv as buildenv

def print_dockerfile(args):
    argparser = argparse.ArgumentParser(
        description="action \"print-dockerfile\": " +
        str(actions()["print-dockerfile"]["description"]))
    argparser.add_argument("env", help="Name of the environment " +
        "of which to print the combined Dockerfile")
    args = argparser.parse_args(args)

    # Get environment:
    envs = buildenv.get_environments()
    env = None
    for _env in envs:
        if _env.name == args.env:
            env = _env
            break
    if env is None:
        print("p4aspaces: error: " +
            "no such environment found: '" + str(args.env) + "'",
            file=sys.stderr, flush=True)
        sys.exit(1)
    print(env.get_docker_file(add_workspace=True))
    sys.exit(0)
