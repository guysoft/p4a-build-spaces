
def actions():
    from p4aspaces.actions.launch_cmd import launch_cmd
    from p4aspaces.actions.launch_shell import launch_shell
    from p4aspaces.actions.list_envs import list_envs

    actions = {
        "shell": {
            "description": "Launch a shell in a given build/testing " +
                "environment, " +
                "use \"list-envs\" for a full list of choices",
            "function": launch_shell,
        },
        "cmd": {
            "description": "Run a command in a given build/testing " +
                "environment.",
            "function": launch_cmd,
        },
        "list-envs": {
            "description": "List all available build/testing environments",
            "function": list_envs,
        },
    }
    return actions

