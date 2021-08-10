#!/usr/bin/python3
"""
a Fabric script that generates a .tgz archive from
the contents of the web_static folder of your AirBnB
Clone repo, using the function do_pack
"""
from fabric.api import *
from datetime import datetime


env.hosts = ['34.74.94.56', '34.74.11.212']
# User name and password should prferably be based
# as environmnt variables rather than explicitly typing them
# here


def do_deploy(archive_path):
    """Deploys a achive to a number of remote hosts
    """

    with settings(warn_only=True):
        path = local("test -e {} && echo True ".format(archive_path), capture=True)
    if not path:
        return False

    file_name = archive_path.split("/")[-1]
    folder_name = file_name.split(".")[0]

    put(archive_path, "/tmp/{}".format(file_name))
    run("mkdir -p /data/web_static/releases/{}/".format(folder_name))
    #exttrackt the tar file
    run("tar -xzf /tmp/{} -C \
         /data/web_static/releases/{}/".format(file_name, folder_name))

    run("rm /tmp/{}".format(file_name))
    run("cp -r /data/web_static/releases/{}/web_static/* \
         /data/web_static/releases/{}/".format(folder_name, folder_name))

    run("rm -fr \
         /data/web_static/releases/{}/web_static/".format(folder_name))

    run("rm -f /data/web_static/current")
    run("ln -sf /data/web_static/releases/{}/ \
         /data/web_static/current".format(folder_name))

    run("chmod -R 755 /data/")

    print("New version deployed!")
