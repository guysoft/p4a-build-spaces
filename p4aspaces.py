#!/usr/bin/python3

import argparse
import os
import shutil
import subprocess
import sys
import tempfile
import uuid
import urllib.parse

from . import buildenv

def main():
    argparser = argparse.ArgumentParser()
    argparser.add_argument("--list-environments",
        default=False, action="store_true",
        help="Just list all environments and then exit",
        dest="list_envs")
    argparser.add_argument("--env",
        default=None, nargs="?",
        help="Specify an environment to use. If not specified, " +
        "it will be prompted for interactively", dest="env")
    argparser.add_argument("--force-redownload-p4a",
        default=False, action="store_true",
        help="Force docker to rebuild from the p4a download step " +
        "(previous step remain cached), to ensure the newest version " +
        "as present in the repo", dest="force_p4a_redownload")
    argparser.add_argument("--force-rebuild",
        default=False, action="store_true",
        help="Force docker to rebuild entire image from scratch, " +
        "without using any caching", dest="clean_image_rebuild")
    argparser.add_argument("--workspace",
        help="Specify a workspace directory to be mounted into the " +
        "build environment at ~/workspace. If not specified, there " +
        "will be no access to files outside of the container",
        default=None, dest="workspace", nargs="?")
    argparser.add_argument("--cmd",
        help="The command to run, defaults to 'bash'. If you want to " +
        "just build the demo app, replace with 'testbuild' (which will " +
        "automatically write it's result to the --output target)",
        default="bash", dest="cmd")
    argparser.add_argument("--output",
        help="Path where to place any .apk encountered after the " +
        "build inside the build environments internal ~/output folder",
        default=None, nargs="?",
        dest="output_file")
    argparser.add_argument("--p4a",
        default=None, nargs="?",
        help="Specify p4a release archive to use, or the branch " +
        "name (like 'master'). Will be prompted for interactively " +
        "if unspecified", dest="p4a_url")
    args = argparser.parse_args()

    # List environments:
    envs = buildenv.get_environments()
    if args.env is None or args.list_envs:
        print("Available environments:")
        for env in envs:
            print(" " + env.name + "\n     " + env.description)
    if args.list_envs:
        sys.exit(0)

    # Test docker availability:
    try:
        output = subprocess.check_output(["docker", "ps"],
            stderr=subprocess.STDOUT)
    except subprocess.CalledProcessError as e:
        print("ERROR: `docker ps` test command failed. " +
            "Is docker running, and do we have access?",
            file=sys.stderr, flush=True)
        sys.exit(1)

    # Choose environment:
    if args.env is None:
        print("")
        env_name = input("Please choose your environment [default=None]:")
    else:
        env_name = args.env
    if len([env for env in envs if env.name == env_name]) == 0:
        print("ERROR: Not a known environment. Aborting.",
              file=sys.stderr, flush=True)
        sys.exit(1)
    env = [env for env in envs if env.name == env_name][0]

    # Choose download target:
    dl_target = "master"
    if args.p4a_url is not None:
        dl_target = args.p4a_url

    # Launch it:
    env.p4a_target = dl_target
    env.launch_shell(force_p4a_refetch=args.force_p4a_redownload,
        output_file=args.output_file, launch_cmd=args.cmd,
        workspace=args.workspace,
        clean_image_rebuild=args.clean_image_rebuild)

if __name__ == "__main__":
    main()


