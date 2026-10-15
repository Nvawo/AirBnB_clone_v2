#!/usr/bin/python3
"""Fabric script that creates and distributes an archive to the web servers"""
from datetime import datetime
from fabric.api import env, local, put, run, settings
import os

env.hosts = env.hosts or ['PUT_WEB_01_IP_HERE', 'PUT_WEB_02_IP_HERE']


def do_pack():
    """Create a .tgz archive of the web_static folder.

    Returns:
        The archive path if it was generated correctly, otherwise None.
    """
    now = datetime.now().strftime("%Y%m%d%H%M%S")
    archive_path = "versions/web_static_{}.tgz".format(now)

    if not os.path.isdir("versions"):
        if local("mkdir -p versions").failed:
            return None

    print("Packing web_static to {}".format(archive_path))
    result = local("tar -cvzf {} web_static".format(archive_path))
    if result.failed:
        return None

    size = os.path.getsize(archive_path)
    print("web_static packed: {} -> {}Bytes".format(archive_path, size))
    return archive_path


def do_deploy(archive_path):
    """Distribute an archive to the web servers.

    Args:
        archive_path: path to the .tgz archive (ex: versions/web_static_x.tgz)

    Returns:
        True if all operations were done correctly, otherwise False.
    """
    if not os.path.isfile(archive_path):
        return False

    file_name = os.path.basename(archive_path)
    name = os.path.splitext(file_name)[0]
    release = "/data/web_static/releases/{}".format(name)
    tmp_path = "/tmp/{}".format(file_name)

    with settings(warn_only=True):
        if put(archive_path, tmp_path).failed:
            return False

        commands = [
            "mkdir -p {}/".format(release),
            "tar -xzf {} -C {}/".format(tmp_path, release),
            "rm {}".format(tmp_path),
            "if [ -d {0}/web_static ]; then "
            "mv {0}/web_static/* {0}/ && rm -rf {0}/web_static; fi".format(
                release),
            "rm -rf /data/web_static/current",
            "ln -s {}/ /data/web_static/current".format(release),
        ]
        for command in commands:
            if run(command).failed:
                return False

    print("New version deployed!")
    return True


def deploy():
    """Create and distribute an archive to the web servers.

    Returns:
        False if no archive was created, otherwise the do_deploy result.
    """
    archive_path = do_pack()
    if archive_path is None:
        return False
    return do_deploy(archive_path)
