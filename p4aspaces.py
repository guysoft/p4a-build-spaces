#!/usr/bin/python3

import argparse
import os
import shutil
import subprocess
import sys
import tempfile
import uuid
import urllib.parse

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
    argparser.add_argument("--p4a",
        default=None, nargs="?",
        help="Specify p4a release archive to use, or the branch " +
        "name (like 'master'). Will be prompted for interactively " +
        "if unspecified", dest="p4a_url")
    args = argparser.parse_args()

    # List environments:
    envs_dir = os.path.abspath(os.path.join(
        os.path.dirname(__file__), "environments"))
    envs = [p for p in os.listdir(envs_dir) if (
        os.path.isdir(os.path.join(envs_dir, p)) and
        os.path.exists(os.path.join(envs_dir, p,
                                    "short_description.txt")) and
        not p.startswith("."))]
    if args.env is None or args.list_envs:
        print("Available environments:")
        for env in sorted(envs):
            desc = open(os.path.join(envs_dir, env, "short_description.txt"), "r",
                        encoding="utf-8").read().strip().partition("\n")[0]
            print(" " + env + "\n     " + desc)
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
        env = input("Please choose your environment [default=None]:")
    else:
        env = args.env
    if not str(env) in envs:
        print("ERROR: Not a known environment. Aborting.",
              file=sys.stderr, flush=True)
        sys.exit(1)
    assert(os.path.exists(os.path.join(envs_dir, env)))

    # Choose download target:
    dl_target = None
    if args.p4a_url is None:
        dl_input = input("Please choose the p4a url download or branch to use\n" +
            "    [default=https://github.com/kivy/python-for-android/archive/master.zip]:")
    else:
        dl_input = args.p4a_url
    if dl_input is None or len(dl_input.strip()) == 0:
        dl_target = "https://github.com/kivy/python-for-android/archive/master.zip"
    elif dl_input.find("/") < 0 and dl_input.find("\\") < 0:  # probably a branch
        dl_target = "https://github.com/kivy/python-for-android/archive/" +\
            urllib.parse.quote(dl_input) + ".zip"
    else:
        dl_target = str(dl_input).strip()

    # Launch it:
    image_name = "p4atestenv-" + str(env)
    temp_d = tempfile.mkdtemp(prefix="p4a-testing-space-")
    try:
        with open(os.path.join(envs_dir, "test_app_instructions.txt"),
                  "r") as f:
            test_app_instructions = f.read().strip()
        with open(os.path.join(envs_dir, env, "Dockerfile"), "r") as f:
            with open(os.path.join(temp_d, "Dockerfile"), "w") as f2:
                f2.write(f.read().replace("{P4A_INSTALL_CMD}",
                    "pip3 install -U '" + str(
                    dl_target.replace("'", "'\"'\"'")) + "'").replace(
                    "{TEST_APP_INSTRUCTIONS}", test_app_instructions))
        # Build container:
        cmd = ["docker", "build",
            "-t", image_name, "--file", os.path.join(
            temp_d, "Dockerfile"), "."]
        if subprocess.call(cmd, cwd=temp_d) != 0:
            print("ERROR: build failed.", file=sys.stderr)
            sys.exit(1)

        # Launch shell:
        cmd = ["docker", "run", "-ti", image_name]
        subprocess.call(cmd)
    finally:
        shutil.rmtree(temp_d)
main()

