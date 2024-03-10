#!/usr/bin/python3
from fabric.api import env, run, local

env.hosts = ["54.237.24.16", "100.26.227.61"]
env.user = "ubuntu"
env.key_filename = "~/.ssh/id_rsa"


def do_clean(number=0):
    """Deletes out-of-date archives.

    Args:
        number (int): The number of archives to keep (default is 0).

    Notes:
        If number is 0 or 1, keep only the most recent version of the archive.
        If number is 2, keep the most recent and second most recent versions of the archive.
        etc.
    """
    number = int(number)
    if number < 0:
        print("Number of archives to keep should be a non-negative integer.")
        return

    # Delete unnecessary archives in the versions folder
    local("ls -t versions | tail -n +{} | xargs -I {{}} rm versions/{{}}".format(number + 1))

    # Delete unnecessary archives in the /data/web_static/releases folder on web servers
    run("cd /data/web_static/releases && ls -t | tail -n +{} | xargs -I {{}} rm -rf /data/web_static/releases/{{}}".format(
        number + 1))
