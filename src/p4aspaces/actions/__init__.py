'''
Copyright (c) 2018-2019 p4a-build-spaces team and others, see AUTHORS.md

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
THE SOFTWARE.
'''

def actions():
    from p4aspaces.actions.launch_cmd import launch_cmd
    from p4aspaces.actions.launch_shell import launch_shell
    from p4aspaces.actions.list_envs import list_envs
    from p4aspaces.actions.print_dockerfile import print_dockerfile

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
        "print-dockerfile": {
            "description": "Print out the combined Dockerfile which " +
                "p4a-build-spaces will use internally for creating " +
                "this environment",
            "function": print_dockerfile,
        }
    }
    return actions

