
from p4aspaces.actions.launch_shell_or_cmd \
    import launch_shell_or_cmd

def launch_cmd(args):
    launch_shell_or_cmd(args, shell=False)

