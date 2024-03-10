from fabric.api import env, run, put
from datetime import datetime

from os.path import exists

env.hosts = ["54.237.24.16", "100.26.227.61"]
env.user = "ubuntu"
env.key_filename = '~/.ssh/id_rsa'


def do_deploy(archive_path):
    """Deploys the archive to web servers."""

    if not exists(archive_path):
        print("Archive not found: {}".format(archive_path))
        return False

    try:
        archive_name = archive_path.split('/')[-1]
        folder_name = archive_name.split('.')[0]

        # Upload the archive to /tmp directory on the web servers
        put(archive_path, '/tmp/{}'.format(archive_name))

        # Uncompress the archive to designated directory
        run('mkdir -p /data/web_static/releases/{}/'.format(folder_name))
        run('tar -xzf /tmp/{} -C /data/web_static/releases/{}/'.format(archive_name, folder_name))

        # Remove the archive from the web servers
        run('rm /tmp/{}'.format(archive_name))

        # Move contents of archive's web_static/ to main web_static directory
        run('mv /data/web_static/releases/{}/web_static/* /data/web_static/'.format(folder_name))
        run('rm -rf /data/web_static/releases/{}/web_static'.format(folder_name))

        # Delete the symbolic link /data/web_static/current
        run('rm -rf /data/web_static/current')

        # Create a new symbolic link /data/web_static/current pointing to the new release
        run('ln -s /data/web_static/releases/{}/ /data/web_static/current'.format(folder_name))

        print("New version deployed!")
        return True

    except Exception as e:
        print("Deployment failed: {}".format(e))
        return False

# Function to generate archive (replace with your actual implementation)
# def do_pack():
#   # Your code to generate the archive and return the archive path
#   # (e.g., using tar or similar tool)
#   pass


# Example usage (uncomment to deploy with a generated archive)
# archive_path = do_pack()
# if archive_path:
#   do_deploy(archive_path)
