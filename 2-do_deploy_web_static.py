from fabric.api import env, run, put
from datetime import datetime

from os.path import exists

env.hosts = ["54.237.24.16", "100.26.227.61"]
env.user = "ubuntu"
env.key_filename = '~/.ssh/id_rsa'


def do_deploy(archive_path):
    if not exists(archive_path):
        return False

    try:
        archive_name = archive_path.split('/')[-1]
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
        return True
    except Exception as e:
        print("Deployment failed: {}".format(e))
        return False
# def deploy():
#     archive_path = 'versions/web_static_{}.tgz'.format(datetime.now().strftime('%Y%m%d%H%M%S'))
#     if not do_pack():
#         print("Failed to create archive.")
#         return False
#     return do_deploy(archive_path)
