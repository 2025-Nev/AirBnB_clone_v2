#!/usr/bin/python3
from fabric.api import env, put, run
import os

# Define the hosts (IP addresses of your web servers)
env.hosts = ['52.86.69.194', '18.209.223.236']

def do_deploy(archive_path):
    """
    Distributes an archive to the web servers.
    Args:
        archive_path: The path to the archive file to be deployed
    Returns:
        True if all operations succeed, False otherwise
    """

    if not os.path.exists(archive_path):
        return False

    # Extract the archive filename and remove its extension
    file_name = archive_path.split('/')[-1]
    file_no_ext = file_name.split('.')[0]

    # Define the destination paths
    tmp_path = '/tmp/{}'.format(file_name)
    release_path = '/data/web_static/releases/{}'.format(file_no_ext)

    try:
        # Upload the archive to the /tmp/ directory of the web server
        put(archive_path, tmp_path)

        # Uncompress the archive to the folder /data/web_static/releases/<archive filename without extension>
        run('mkdir -p {}'.format(release_path))
        run('tar -xzf {} -C {}'.format(tmp_path, release_path))

        # Delete the archive from the web server
        run('rm {}'.format(tmp_path))

        # Move the contents of the web_static folder to the release path
        run('mv {}/web_static/* {}'.format(release_path, release_path))

        # Remove the empty web_static folder
        run('rm -rf {}/web_static'.format(release_path))

        # Delete the old symbolic link
        run('rm -rf /data/web_static/current')

        # Create a new symbolic link
        run('ln -s {} /data/web_static/current'.format(release_path))

        print("New version deployed!")
        return True

    except Exception as e:
        print("Deployment failed:", e)
        return False
