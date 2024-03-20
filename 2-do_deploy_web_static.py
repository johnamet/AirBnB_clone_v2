#!/usr/bin/python3
""" Fabric script that distributes an archive to the web servers

    Usage: fab -f 2-do_deploy_web_static.py do_deploy:archive_path=path
           -i path to private key

    ex: fab -f 2-do_deploy_web_static.py do_deploy:archive_path=versions/we
        b_static_20240307104334.tgz -i ~/.ssh/id_rsa
"""
from fabric.api import *
import os


env.hosts = ['', '18.233.66.83']
env.user = "ubuntu"


def do_deploy(archive_path):
    """ distributes an archive to the web servers """

    # archive_path: versions/web_static_20240307104334.tgz
    if not os.path.exists(archive_path):
        return False

    # upload the archive to /tmp/ on the web servers
    put(archive_path, '/tmp/')

    # file: web_static_20240307104334.tgz
    file = archive_path.split('/')[-1]

    # folder: web_static_20240307104334: contains all the files
    folder = file.split('.')[0]

    try:
        # uncompress the archive to /data/web_static/releases/filename
        run('mkdir -p /data/web_static/releases/{}/'.format(folder))
        run('tar -xzf /tmp/{} -C /data/web_static/releases/{}/'.
            format(file, folder))

        # delete archive (web_static_20240307104334.tgz) from the web server
        run('rm /tmp/{}'.format(file))

        # move contents of web_static folder up one level
        """ before:                           after:
            /data/web_static/releases/folder/ /data/web_static/releases/folder/
            │                                 |
            └── web_static/                   ├── 0-index.html
                ├── 0-index.html              ├── 1-index.html
                ├── 1-index.html              └── images/
                └── images/                       └── logo.png
                    └── logo.png
        """

        run('mv /data/web_static/releases/{}/web_static/* '
            '/data/web_static/releases/{}/'.format(folder, folder))

        # remove now-empty web_static directory
        run('rm -rf /data/web_static/releases/{}/web_static'.format(folder))

        # delete the symbolic link /data/web_static/current from the web server
        run('rm -rf /data/web_static/current')

        # create a new symbolic link /data/web_static/current to new version
        run('ln -s /data/web_static/releases/{}/ /data/web_static/current'.
            format(folder))

        print("New version deployed!")

        return True
    except Exception as e:
        return False