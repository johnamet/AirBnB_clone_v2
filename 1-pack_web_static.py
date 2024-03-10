#!/usr/bin/python3
from fabric import task
from datetime import datetime
import os

@task
def do_pack(c):
    """Packs contents of web_static into a .tgz archive."""
    time_format = "%Y%m%d%H%M%S"
    now = datetime.utcnow().strftime(time_format)
    archive_name = "web_static_{}.tgz".format(now)
    folder_path = "versions"

    # Create the versions folder if it doesn't exist
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)

    # Command to create the .tgz archive
    tar_command = "tar -cvzf {}/{} web_static".format(folder_path, archive_name)

    # Run the tar command
    result = c.local(tar_command)

    # Check if the command executed successfully
    if result.failed:
        return None
    else:
        return os.path.join(folder_path, archive_name)
