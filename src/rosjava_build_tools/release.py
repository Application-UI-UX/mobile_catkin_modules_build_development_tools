#!/usr/bin/env python

##############################################################################
# Imports
##############################################################################

import rosdistro
import catkin_pkg

##############################################################################
# Imports
##############################################################################


def has_build_depend_on_message_generation(package):
    '''
      Checks for a build dependency on message generation to determine if
      that package contains msgs/srvs.

      @param package : typical catkin package object
      @type catkin_pkg.Package

      @return True if it is a package that contains msgs/srvs
      @rtype Bool
    '''
    return 'message_generation' in [d.name for d in package.build_depends]


def scrape_for_release_message_packages(track):
    url = rosdistro.get_index_url()
    index = rosdistro.get_index(url)
    cache = rosdistro.get_release_cache(index, 'hydro')
    packages = []
    for package_name, package_string in cache.package_xmls.iteritems():
        package = catkin_pkg.package.parse_package_string(package_string)
        #print("  Name: %s" % package_name)
        #print("  Buildtool Depends %s" % package.build)
        if has_build_depend_on_message_generation(package):
            packages.append({'name': package_name, 'version': package.version})
    return packages
