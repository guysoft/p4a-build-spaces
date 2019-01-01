
## p4a build spaces

**`p4a-build-spaces` allows you to launch an interactive
shell** with a reproducible build and test environment with
[https://github.com/kivy/python-for-android](python-for-android).

**Still in development / unstable.**

### Installation

1. Install [https://docker.io](docker), e.g. as described here:

https://www.digitalocean.com/community/tutorials/how-to-install-and-use-docker-on-ubuntu-18-04

2. install p4a build spaces:

`pip install -U https://github.com/JonasT/p4a-build-spaces/archive/master.zip`

**If you have both `pip2`/`pip3`, use `pip3`!** (Python 2 is not supported)

### Launch

Before you launch, make sure docker is running! (`sudo service docker start`)

1. List environments: `p4aspaces list-envs`
2. Launch shell with your choice: `p4aspaces shell p4a-py3-api28ndk21`

**Important:** All file changes are temporary and will be lost once
the environment terminates, unless you added a `--workspace`.
(p4a build spaces always launches a *new* container,
and attempts to delete it after your shell terminates to give you
a clean environment next time)

### Launch without install

You can run directly out of the `p4a-build-spaces` extracted tarball /
development folder without installing system-wide. Just use:

  1. `chmod +x ./p4aspaces`,
  2. `./p4aspaces ...` (instead of `p4sapaces`).

### Cleanup

Please note the docker images will be left around, one per environment
you used. Also, the containers will be terminated, but also left around.
This will use up disk space.

To remove the used disk space, use: `sudo docker system prune`

**(warning: if you use docker for something else, stopped containers
and unused volumes of that may be removed as well!!)**


