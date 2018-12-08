
import argparse
import subprocess
import sys

from p4aspaces.actions import actions
import p4aspaces.buildenv as buildenv

def launch_shell_or_cmd(args, shell=False):
    if shell:
        argparser = argparse.ArgumentParser(
            description="action \"shell\": " +
            str(actions()["shell"]["description"]))
    else:
        argparser = argparse.ArgumentParser(
            description="action \"cmd\": " +
            str(actions()["cmd"]["description"]))
    argparser.add_argument("env",
        default=None, nargs=1,
        help="Specify an environment to use.")
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
    if not shell:
        argparser.add_argument("command", nargs=1,
            help="The command to run, defaults to 'bash'. If you want to " +
            "just build the demo app, replace with 'testbuild' (which will " +
            "automatically write it's result to the --output target)",
            default="bash")
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
    args = argparser.parse_args(args)
    if shell:
        args.command = "bash"
        args.output_file = None
    else:
        if len(args.command) > 0:
            args.command = args.command[0]
    if len(args.env) > 0:
        args.env = args.env[0]

    # List environments:
    envs = buildenv.get_environments()

    # Test docker availability:
    try:
        output = subprocess.check_output(["docker", "ps"],
            stderr=subprocess.STDOUT)
    except (subprocess.CalledProcessError,
            FileNotFoundError) as e:
        print("p4aspaces: error: `docker ps` test command failed. " +
            "\n       Is docker running, and do we have access?",
            file=sys.stderr, flush=True)
        sys.exit(1)

    # Choose environment:
    env_name = args.env
    if len([env for env in envs if env.name == env_name]) == 0:
        print("p4aspaces: error: Not a known environment. Aborting.",
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
        output_file=args.output_file, launch_cmd=args.command,
        workspace=args.workspace,
        clean_image_rebuild=args.clean_image_rebuild)

