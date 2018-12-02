#!/usr/bin/python3

import os
import shutil
import subprocess
import sys
import tempfile
import uuid

def main():
    # Test docker availability:
    try:
        output = subprocess.check_output(["docker", "ps"],
            stderr=subprocess.STDOUT)
    except subprocess.CalledProcessError as e:
        print("ERROR: `docker ps` test command failed. " +
            "Is docker running, and do we have access?",
            file=sys.stderr, flush=True)
        sys.exit(1)

    envs_dir = os.path.abspath(os.path.join(
        os.path.dirname(__file__), "environments"))
    envs = [p for p in os.listdir(envs_dir) if (
        os.path.isdir(os.path.join(envs_dir, p)) and
        os.path.exists(os.path.join(envs_dir, p,
                                    "short_description.txt")) and
        not p.startswith("."))]
    print("Available environments:")
    for env in sorted(envs):
        desc = open(os.path.join(envs_dir, env, "short_description.txt"), "r",
                    encoding="utf-8").read().strip().partition("\n")[0]
        print(" " + env + "\n     " + desc)
    print("")
    env = input("Please choose your environment [default=None]:")
    if not str(env) in envs:
        print("ERROR: Not a known environment. Aborting.",
              file=sys.stderr, flush=True)
        sys.exit(1)
    assert(os.path.exists(os.path.join(envs_dir, env)))

    dl_target = None
    dl_input = input("Please choose the p4a version to use\n" +
        "    [default=https://github.com/kivy/python-for-android/archive/master.zip]:")
    if dl_input is None or len(dl_input.strip()) == 0:
        dl_target = "https://github.com/kivy/python-for-android/archive/master.zip"
    else:
        dl_target = str(dl_input).strip()

    # Launch it:
    image_name = "p4atestenv-" + str(uuid.uuid4()).replace("-", "")
    temp_d = tempfile.mkdtemp(prefix="p4a-testing-space-")
    try:
        with open(os.path.join(envs_dir, env, "Dockerfile"), "r") as f:
            with open(os.path.join(temp_d, "Dockerfile"), "w") as f2:
                f2.write(f.read().replace("{P4A_INSTALL_CMD}",
                    "pip3 install -U '" + str(
                    dl_target.replace("'", "'\"'\"'")) + "'"))
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

