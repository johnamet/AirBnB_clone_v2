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
    os.chdir("/data/web_static/current")  # Change directory to your web_static folder
    Handler = http.server.SimpleHTTPRequestHandler
    with socketserver.TCPServer(("localhost", 8000), Handler) as httpd:
        print("Server started at http://localhost:8000/")
        httpd.serve_forever()


def update_symbolic_link(archive_filename):
    try:
        # Remove existing current symbolic link
        os.remove("/data/web_static/current")

        # Create new symbolic link pointing to the new archive version
        os.symlink(archive_filename, "/data/web_static/current")
        print(f"Symbolic link updated to {archive_filename}")
    except Exception as e:
        print(f"Failed to update symbolic link: {e}")


def do_deploy(archive_path):
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
        update_symbolic_link(os.path.basename('/data/web_static/releases/{}/'.format(folder_name)))
        expose_index_thread = threading.Thread(target=expose_index_locally)
        expose_index_thread.start()

        return True
    except Exception as e:
        print("Deployment failed: {}".format(e))
        return False

#
# if __name__ == "__main__":
#     # Expose 0-index.html and my-index.html locally
#     expose_index_thread = threading.Thread(target=expose_index_locally)
#     expose_index_thread.start()
#
#     # Deploy the archive and update symbolic link
#     archive_path = 'path/to/your/archive.tgz'  # Replace with the path to your archive
#     do_deploy(archive_path)
