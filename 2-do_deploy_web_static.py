#!/usr/bin/python3
from fabric.api import run, env, put, sudo, local

# Define the web server IPs
env.hosts = ["54.237.24.16 web-01", "100.26.227.61 web-02"]


def do_deploy(archive_path):
    """Deploys the archive to web servers.

    Args:
        archive_path (str): Path to the archive file.

    Returns:
        bool: True if deployment is successful, False otherwise.
    """
    # Check if the archive file exists
    if not local("test -f {}".format(archive_path)):
        print("Archive not found: {}".format(archive_path))
        return False

    # Upload archive to /tmp/ on web servers
    with env.hosts:
        print(f"Uploading archive to web servers: {archive_path} -> /tmp/")
        try:
            put(archive_path, "/tmp/")
        except:
            print("Error uploading archive to web servers.")
            return False

    # Extract archive on web servers
    archive_filename = archive_path.split("/")[-1]
    release_dir = f"/data/web_static/releases/{archive_filename.replace('.tgz', '')}"
    with env.hosts:
        print(f"Extracting archive on web servers. Release directory: {release_dir}")
        try:
            run(f"tar -xzf /tmp/{archive_filename} -C /data/web_static/releases/")
        except:
            print(f"Error extracting archive on web servers. Release directory: {release_dir}")
            return False

    # Delete archive from web servers
    with env.hosts:
        print("Deleting archive from web servers.")
        try:
            run(f"rm /tmp/{archive_filename}")
        except:
            print("Error deleting archive from web servers.")
            return False

    # Delete and recreate symbolic link
    with env.hosts:
        print("Updating symbolic link on web servers.")
        try:
            sudo("rm /data/web_static/current")
            sudo(f"ln -s {release_dir} /data/web_static/current")
        except:
            print("Error updating symbolic link on web servers.")
            return False

    print("Deployment successful!")
    return True

# Example usage (uncomment to run locally)
# archive_path = "/path/to/your/archive.tgz"
# do_deploy(archive_path)
