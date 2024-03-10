from fabric.api import run, env, local, put, sudo

env.hosts = ['54.237.24.16 web-01', '100.26.227.61 web-02>']  # Replace with actual IPs


def do_deploy(archive_path):
    """Deploys the archive to web servers with progress messages."""

    print("Checking archive...")
    if not local("test -f {}".format(archive_path)):
        print("Archive not found: {}".format(archive_path))
        return False

    print("Uploading archive to web servers...")
    with env.hosts:
        try:
            put(archive_path, "/tmp/")
        except:
            print("Error uploading archive to web servers.")
            return False
    print("Upload complete.")

    archive_filename = archive_path.split("/")[-1]
    release_dir = f"/data/web_static/releases/{archive_filename.replace('.tgz', '')}"

    print("Extracting archive on web servers...")
    with env.hosts:
        try:
            run(f"tar -xzf /tmp/{archive_filename} -C /data/web_static/releases/")
        except:
            print(f"Error extracting archive on web servers. Release directory: {release_dir}")
            return False
    print("Extraction complete.")

    print("Deleting uploaded archive...")
    with env.hosts:
        try:
            run(f"rm /tmp/{archive_filename}")
        except:
            print("Error deleting archive from web servers.")
            return False
    print("Archive deletion complete.")

    print("Updating symbolic link...")
    with env.hosts:
        try:
            sudo("rm /data/web_static/current")
            sudo(f"ln -s {release_dir} /data/web_static/current")
        except:
            print("Error updating symbolic link on web servers.")
            return False
    print("Symbolic link updated.")

    print("Deployment successful!")
    return True
