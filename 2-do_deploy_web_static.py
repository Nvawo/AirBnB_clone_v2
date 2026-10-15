#!/usr/bin/python3
"""Fabric script that distributes an archive to the web servers"""
from fabric.api import env, put, run, settings
import os

env.hosts = ['WEB_01_IP', 'WEB_02_IP']


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
