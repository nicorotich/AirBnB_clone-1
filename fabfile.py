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
#env.hosts = ['34.74.94.56', '34.74.11.212']
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
        local("tar -cvzf versions/%s %s" % (env.arc_name, env.arc_src), capture=False)
        return env.arc_src+"/versions/{}".format(env.arc_name)
    except:
        return None

def do_deploy(archive_path):
    """Deploys a achive to a number of remote hosts
    """ 
    
    path_stat = local("if [[ -e %s ]]; then echo 1;else echo 0; fi ", capture=True)
    print(path_stat)
