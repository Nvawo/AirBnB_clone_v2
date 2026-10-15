#!/usr/bin/python3
"""Fabric script that generates a .tgz archive from web_static"""
from datetime import datetime
from fabric.api import local
import os


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
