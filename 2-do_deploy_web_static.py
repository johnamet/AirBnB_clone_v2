#!/usr/bin/python3
"""
Fabric script (based on the file 1-pack_web_static.py)
"""

from fabric.api import env, put, run
from os.path import exists
# Define the web server IPs
env.hosts = ["54.237.24.16 web-01", "100.26.227.61 web-02"]

def do_deploy(archive_path):
    """
    Distributes an archive to your web servers
    """
    if not exists(archive_path):
        return False

    try:
        archive_name = archive_path.split('/')[-1]
        archive_folder = archive_name.split('.')[0]

        put(archive_path, '/tmp/')
        run('mkdir -p /data/web_static/releases/{}/'.format(archive_folder))
        run('tar -xzf /tmp/{} -C /data/web_static/releases/{}/'
            .format(archive_name, archive_folder))
        run('rm /tmp/{}'.format(archive_name))
        run('mv /data/web_static/releases/{}/web_static/* '
            '/data/web_static/releases/{}/'.format(archive_folder, archive_folder))
        run('rm -rf /data/web_static/releases/{}/web_static'
            .format(archive_folder))
        run('rm -rf /data/web_static/current')
        run('ln -s /data/web_static/releases/{}/ /data/web_static/current'
            .format(archive_folder))
        print("New version deployed!")
        return True
    except Exception as e:
        print(e)
        return False
