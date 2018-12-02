
## p4a testing spaces

This project contains a script & various Dockerfile's to launch an interactive
shell with a reproducible environment with python-for-android.

It is meant to allow testing various Android SDK, NDK and python version
combinations quickly.

### Usage

#### Interactive Environment Choice

Run `./testenv.py` which will ask you for the environment interactively.

#### Arguments Quick Setup

You can choose an environment with launch arguments right away:

Example: `./testenv.py --env p4a-py3-api18ndk21 --p4a master`

(Uses `p4a`'s master branch from github with environment
`p4a-py3-api18ndk21`. Use `./testenv.py --list-environments` for
a full list.)

