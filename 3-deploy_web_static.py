#!/usr/bin/python3
"""
Fabric script (based on the file 2-do_deploy_web_static.py)
"""

from fabric.api import env, local, run
from datetime import datetime
import os

# Define the web server IPs
env.hosts = ["54.237.24.16 web-01", "100.26.227.61 web-02"]


def do_pack():
    """
    Generates a .tgz archive from the contents of the web_static folder.

    Returns:
        str: Path to the created archive, or None if the archiving failed.
    """
    try:
        current_time = datetime.now().strftime('%Y%m%d%H%M%S')
        archive_name = f'web_static_{current_time}.tgz'
        local('mkdir -p versions')
        local(f'tar -czvf versions/{archive_name} web_static')
        return f'versions/{archive_name}'
    except Exception as e:
        print(f"Error during archiving: {e}")
        return None


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
        print("Uploading archive to web servers...")
        # Upload the archive to /tmp/ directory on the web server
        put(archive_path, '/tmp/')
        print(f"Archive uploaded successfully. ({archive_path})")

        # Extract the archive to /data/web_static/releases/
        filename = os.path.basename(archive_path)
        folder_name = filename.split('.')[0]
        release_path = f'/data/web_static/releases/{folder_name}'
        print("Extracting archive on web servers...")
        run(f'mkdir -p {release_path}')
        run(f'tar -xzf /tmp/{filename} -C {release_path}')
        print("Archive extracted successfully.")

        # Delete the archive from the web server
        print("Deleting archive from web servers...")
        run(f'rm /tmp/{filename}')
        print("Archive deleted successfully.")

        # Remove the existing symbolic link
        print("Updating symbolic link on web servers...")
        current_link = '/data/web_static/current'
        run(f'rm -f {current_link}')

        # Create a new symbolic link to the new version
        run(f'ln -s {release_path} {current_link}')
        print("Symbolic link updated successfully.")

        print("Deployment successful!")
        return True
    except Exception as e:
        print(f"Error during deployment: {e}")
        return False


def deploy():
    """
    Deploys the web_static content to the web servers.

    Returns:
        bool: True if deployment is successful, False otherwise.
    """
    # Create archive
    archive_path = do_pack()
    if not archive_path:
        print("No archive created. Deployment failed.")
        return False

    # Deploy archive
    return do_deploy(archive_path)
