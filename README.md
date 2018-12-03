
## p4a build spaces

**`p4a-build-spaces` allows you to launch an interactive
shell** with a reproducible build and test environment with
[https://github.com/kivy/python-for-android](python-for-android).

**Still in development / unstable.**

### Installation

Run:

`pip install -U https://github.com/JonasT/p4a-build-spaces/archive/master.zip`

... to install the latest dev version (unstable!).
**(If you have both Python 2 and Python 3 pip, make sure to install with `pip3`!)**

### Launch

Run:

`p4spaces`

You will be prompted for the environment interactively.
After setup has completed, you will be dropped to a `bash` shell inside
your testing environment!

**Don't forget that all file changes are temporary and will be lost once
the environment terminates, unless you added a `--workspace`.**

### Launch Quickly

Run:

`p4aspaces --env p4a-py3-api28ndk21 --p4a master`

...or similar, to skip the interactive part and get an env right away.

(Prepares `p4a`'s master branch from github with environment
`p4a-py3-api28ndk21`. Use `./p4aspaces.py --list-environments` for
a full list.)

### Cleanup

Please note the docker images will be left around, one per environment
you used. Also, the containers will be left around.

To clean up, use: `sudo docker system prune`

**(warning: if you use docker for something else, stopped containers
and unused volumes of that may be removed as well!!)**


