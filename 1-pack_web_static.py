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
        local("tar -cvzf versions/{} {}".format(env.arc_name, env.arc_src),
              capture=False)
        return env.arc_src+"/versions/{}".format(env.arc_name)
    except:
        return None
