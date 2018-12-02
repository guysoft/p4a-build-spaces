
## p4a testing spaces

This project contains a script & various Dockerfile's to launch an interactive
shell with a reproducible environment with python-for-android.

It is meant to allow testing various Android SDK, NDK and python version
combinations quickly.

### Usage

#### Interactive Environment Choice

Run `./p4aspaces.py` which will ask you for the environment interactively.
After setup has completed, you will be dropped to a `bash` shell inside
your testing environment!

#### Arguments Quick Setup

You can choose an environment with launch arguments right away:

Example: `./p4aspaces.py --env p4a-py3-api18ndk21 --p4a master`

(Uses `p4a`'s master branch from github with environment
`p4a-py3-api18ndk21`. Use `./p4aspaces.py --list-environments` for
a full list.)

#### Cleanup

Please note the docker images will be left around, one per environment
you used. Also, the containers will be left around.

To clean up, use: `sudo docker system prune`

**(warning: if you use docker for something else, stopped containers
and unused volumes of that may be removed as well!!)**


