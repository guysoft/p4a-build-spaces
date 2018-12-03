
import os
from .settings import settings
import shutil
import subprocess
import sys
import tempfile
import uuid
import urllib.parse

class BuildEnvironment(object):
    def __init__(self, folder_path, envs_base_dir,
            p4a_target="master"):
        self.path = os.path.normpath(os.path.abspath(folder_path))
        if not os.path.exists(folder_path):
            raise RuntimeError("BuildEnvironment() needs " +
                "valid, existing base folder: " + str(folder_path))
        self.name = os.path.basename(self.path)
        self.envs_dir = envs_base_dir
        self.p4a_target = p4a_target
        self.description = open(
            os.path.join(self.path, "short_description.txt"),
            "r",
            encoding="utf-8"
        ).read().strip().partition("\n")[0]

    def get_docker_file(self, force_p4a_refetch=False, launch_cmd="bash",
            start_dir="/root/"):
        image_name = "p4atestenv-" + str(self.name)

        # Obtain p4a build uuid (to control docker caching):
        env_settings = settings.get("environments", type=dict)
        if not self.name in env_settings:
            env_settings[self.name] = dict()
        if not "last_build_p4a_uuid" in env_settings[self.name] or \
                force_p4a_refetch:
            build_p4a_uuid = str(uuid.uuid4())
        else:
            build_p4a_uuid = env_settings[self.name]["last_build_p4a_uuid"]
        env_settings[self.name]["last_build_p4a_uuid"] = build_p4a_uuid
        settings.set("environments", env_settings)

        dl_target = self.p4a_target
        if dl_target is None or len(dl_target.strip()) == 0:
            dl_target = "https://github.com/kivy/python-for-android/" +\
                        "archive/master.zip"
        elif dl_target.find("/") < 0 and \
                dl_target.find("\\") < 0:  # probably a branch
            dl_target = "https://github.com/kivy/python-for-android/" +\
                "archive/" + urllib.parse.quote(dl_target) + ".zip"
        else:
            dl_target = str(dl_target).strip()

        with open(os.path.join(self.envs_dir, "test_app_instructions.txt"),
                  "r") as f:
            test_app_instructions = f.read().strip()
        with open(os.path.join(self.path, "Dockerfile"), "r") as f:
            return f.read().replace("{P4A_INSTALL_CMD}",
                "$PIP install -U '" + str(
                dl_target.replace("'", "'\"'\"'")) + "'  # " +
                "p4a build " + str(build_p4a_uuid)).replace(
                "{TEST_APP_INSTRUCTIONS}", test_app_instructions).replace(
                "{LAUNCH_CMD}",
                launch_cmd.replace("\\", "\\\\").replace(
                "\"", "\\\"").replace("\n", "\\n").replace(
                "\r", "\\r").replace("'", "'\"'\"'")).replace(
                "{START_DIR}", start_dir)

    def launch_shell(self, force_p4a_refetch=False, launch_cmd="bash",
            output_file=None, workspace=None):
        # Build container:
        image_name = "p4atestenv-" + str(self.name)
        container_name = image_name + "-" +\
            str(uuid.uuid4()).replace("-", "")
        temp_d = tempfile.mkdtemp(prefix="p4a-testing-space-")
        try:
            os.mkdir(os.path.join(temp_d, "output"))
            with open(os.path.join(temp_d, "Dockerfile"), "w") as f:
                f.write(self.get_docker_file(
                    force_p4a_refetch=force_p4a_refetch,
                    launch_cmd=launch_cmd,
                    start_dir=("/root/" if workspace is None else \
                                        "/root/workspace/")
                ))
            
            # Build container:
            cmd = ["docker", "build",
                "-t", image_name, "--file", os.path.join(
                temp_d, "Dockerfile"), "."]
            if subprocess.call(cmd, cwd=temp_d) != 0:
                print("ERROR: build failed.", file=sys.stderr)
                sys.exit(1)

            # Launch shell:
            workspace_volume_args = []
            if args.workspace != None:
                workspace_volume_args += ["-v",
                    os.path.abspath(args.workspace) +
                    ":/root/workspace:rw,Z"]
            cmd = ["docker", "run",
                "--name" + container_name, "-ti",
                "-v", os.path.join(temp_d, "output")] +\
                workspace_volume_args + [
                ":/root/output:rw,Z",
                image_name]
            subprocess.call(cmd)
            if output_file is not None:
                for f in os.listdir(os.path.join(temp_d, "output")):
                    full_path = os.path.join(temp_d, "output", f)
                    if not os.path.isdir(full_path) and f.endswith(".apk"):
                        shutil.copyfile(full_path, output_file)
                        return
        finally:
            try:
                os.system("docker kill " + container_name)
            finally:
                shutil.rmtree(temp_d)

def get_environments(for_p4a_target="master"):
    envs_dir = os.path.abspath(os.path.join(
        os.path.dirname(__file__), "environments"))
    env_names = [p for p in os.listdir(envs_dir) if (
        os.path.isdir(os.path.join(envs_dir, p)) and
        os.path.exists(os.path.join(envs_dir, p,
                                    "short_description.txt")) and
        not p.startswith("."))]
    result = [BuildEnvironment(os.path.join(envs_dir, env_name),
                               envs_dir,
                               p4a_target=for_p4a_target) \
              for env_name in sorted(env_names)]
    return result
