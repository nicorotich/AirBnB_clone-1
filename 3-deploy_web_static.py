#!/usr/bin/python3
"""
a Fabric script that generates a .tgz archive from
the contents of the web_static folder of your AirBnB
Clone repo, using the function do_pack
"""
from fabric.api import *
from datetime import datetime


env.arc_src = './web_static'
env.arc_name = 'web_static_.tgz'
env.hosts = ['34.74.94.56', '34.74.11.212']
# User name and password should prferably be based
# as environmnt variables rather than explicitly typing them
# here


def do_pack():
    """ Packages soruce code into a compressed archive
    """
    global env

    try:

        now = datetime.now()
        tstr = now.strftime("%Y%m%d%H%M%S")
        env.arc_name = 'web_static_{}.tgz'.format(tstr)

        print("Packing web_static to versions/{}".format(env.arc_name))

        local("if test ! -d ./versions; then mkdir versions;fi")
        local("tar -cvzf versions/{} \
               {}".format(env.arc_name, env.arc_src), capture=False)
        return env.arc_src+"/versions/{}".format(env.arc_name)
    except:
        return None


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


def deploy():
    """Packages and deployes source code
    """

    archive_path = do_pack()
    if not archive_path:
        return False
    return do_deploy(archive_path)
