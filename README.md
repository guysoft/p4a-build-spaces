
## p4a build spaces

**`p4a-build-spaces` allows you to launch an interactive
shell** with a reproducible build and test environment with
[https://github.com/kivy/python-for-android](python-for-android).

**Still in development / unstable.**

### Installation

Run:

`pip install -U https://github.com/JonasT/p4a-build-spaces/archive/master.zip`

... to install the latest dev version (unstable!).
**If you have both Python 2 and Python 3 pip, make sure to install with `pip3`!**

### Launch

1. List environments: `p4spaces list-envs`
2. Launch shell with your choice: `p4aspaces shell p4a-py3-api28ndk21`

**Important note:**

All file changes are temporary and will be lost once
the environment terminates, unless you added a `--workspace`.

*Note for testing:*

You can run directly out of the `p4a-build-spaces` development folder
without installing the package by doing `chmod +x ./p4aspaces`,
then using `./p4aspaces` (instead of the system-wide `p4sapaces`).

### Cleanup

Please note the docker images will be left around, one per environment
you used. Also, the containers will be terminated, but also left around.
This will use up disk space.

To remove the used disk space, use: `sudo docker system prune`

**(warning: if you use docker for something else, stopped containers
and unused volumes of that may be removed as well!!)**


