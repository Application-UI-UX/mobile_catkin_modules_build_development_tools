#!/usr/bin/env python

##############################################################################
# Imports
##############################################################################

import rosdistro
import catkin_pkg
from . import catkin

##############################################################################
# Imports
##############################################################################


def scrape_for_release_message_packages(track):
    url = rosdistro.get_index_url()
    index = rosdistro.get_index(url)
    cache = rosdistro.get_release_cache(index, 'kinetic')
    packages = []
    for package_name, package_string in cache.package_xmls.iteritems():
        package = catkin_pkg.package.parse_package_string(package_string)
        #print("  Name: %s" % package_name)
        #print("  Buildtool Depends %s" % package.build)
        if catkin.has_build_depend_on_message_generation(package):
            packages.append({'name': package_name, 'version': package.version})
    return packages
