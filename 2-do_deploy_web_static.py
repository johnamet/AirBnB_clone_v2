#!/usr/bin/python3
import os
import http.server
import socketserver
import threading
from fabric.api import env, run, put
from datetime import datetime

env.hosts = ["54.237.24.16", "100.26.227.61"]
env.user = "ubuntu"
env.key_filename = '~/.ssh/id_rsa'


def expose_index_locally():
    """
  Exposes the index file locally using a Python HTTP server.

  This function serves files from the /data/web_static/current directory
  and exposes them locally on port 8000.

  Example:
      To expose the index file, call expose_index_locally().

  Returns:
      None
  """
    os.chdir("/data/web_static/current")  # Change directory to your web_static folder
    Handler = http.server.SimpleHTTPRequestHandler
    with socketserver.TCPServer(("localhost", 8000), Handler) as httpd:
        print("Server started at http://localhost:8000/")
        httpd.serve_forever()


def update_symbolic_link(archive_filename):
    """
  Updates the symbolic link to point to the new archive version.

  This function removes the existing /data/web_static/current symbolic link
  and creates a new symbolic link pointing to the provided archive filename.

  Args:
      archive_filename (str): The filename of the new archive.

  Example:
      To update the symbolic link, call update_symbolic_link('web_static_20240310120000.tgz').

  Returns:
      None
  """
    try:
        # Remove existing current symbolic link
        os.remove("/data/web_static/current")

        # Create new symbolic link pointing to the new archive version
        os.symlink(archive_filename, "/data/web_static/current")
        print(f"Symbolic link updated to {archive_filename}")
    except Exception as e:
        print(f"Failed to update symbolic link: {e}")


def do_deploy(archive_path):
    """
  Deploys the archive to the web servers and updates the symbolic link.

  This function uploads the specified archive to the remote web servers,
  extracts its contents, moves them to the appropriate directory, and
  updates the symbolic link to point to the new version.

  Args:
      archive_path (str): The path to the archive to be deployed.

  Example:
      To deploy an archive, call do_deploy('/path/to/your/archive.tgz').

  Returns:
      bool: True if the deployment was successful, False otherwise.
  """
    if not os.path.exists(archive_path):
        return False

    try:
        archive_name = os.path.basename(archive_path)
        folder_name = archive_name.split('.')[0]

        # Upload the archive to /tmp directory on the web servers
        put(archive_path, '/tmp/{}'.format(archive_name))

        # Uncompress the archive to /data/web_static/releases/<archive filename without extension>
        run('mkdir -p /data/web_static/releases/{}/'.format(folder_name))
        run('tar -xzf /tmp/{} -C /data/web_static/releases/{}/'.format(archive_name, folder_name))

        # Remove the archive from the web servers
        run('rm /tmp/{}'.format(archive_name))

        # Move contents of web_static/ to new folder and remove original folder
        run('mv /data/web_static/releases/{}/web_static/* /data/web_static/releases/{}/'.format(folder_name,
                                                                                                folder_name))
        run('rm -rf /data/web_static/releases/{}/web_static'.format(folder_name))

        # Delete the symbolic link /data/web_static/current
        run('rm -rf /data/web_static/current')

        # Create a new symbolic link /data/web_static/current
        run('ln -s /data/web_static/releases/{}/ /data/web_static/current'.format(folder_name))

        print("New version deployed!")
        # update_symbolic_link(os.path.basename('/data/web_static/releases/{}/'.format(folder_name)))
        # expose_index_thread = threading.Thread(target=expose_index_locally)
        # expose_index_thread.start()

        return True
    except Exception as e:
        print("Deployment failed: {}".format(e))
        return False
