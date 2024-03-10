#!/usr/bin/python3
"""
Fabric script (based on the file 1-pack_web_static.py)
"""


from fabric.api import env, put, run, local
import os

# Define the web server IPs
env.hosts = ["54.237.24.16 web-01", "100.26.227.61 web-02"]


def do_deploy(archive_path):
    """
    Distributes an archive to web servers and deploys it.

    Args:
        archive_path (str): Path to the archive file.

    Returns:
        bool: True if successful, False otherwise.
    """
    if not os.path.exists(archive_path):
        print(f"Error: Archive file '{archive_path}' does not exist.")
        return False

    try:
        # Upload the archive to /tmp/ directory on the web server
        put(archive_path, '/tmp/')

        # Extract the archive to /data/web_static/releases/
        filename = os.path.basename(archive_path)
        folder_name = filename.split('.')[0]
        release_path = f'/data/web_static/releases/{folder_name}'
        run(f'mkdir -p {release_path}')
        run(f'tar -xzf /tmp/{filename} -C {release_path}')

        # Delete the archive from the web server
        run(f'rm /tmp/{filename}')

        # Remove the existing symbolic link
        current_link = '/data/web_static/current'
        run(f'rm -f {current_link}')

        # Create a new symbolic link to the new version
        run(f'ln -s {release_path} {current_link}')

        print("Deployment successful!")
        return True
    except Exception as e:
        print(f"Error during deployment: {e}")
        return False
