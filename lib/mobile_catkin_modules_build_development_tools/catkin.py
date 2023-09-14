#!/usr/bin/env python

##############################################################################
# Imports
##############################################################################

import os
import catkin_pkg.packages
import catkin_pkg.topological_order

##############################################################################
# Constants
##############################################################################

# packages that don't properly identify themselves as message packages (fix upstream).
message_package_whitelist = ['map_store']

##############################################################################
# Methods
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


def index_message_package_dependencies_from_local_environment(package_name_list=[], package_paths=None):
    '''
      Returns a topologically sorted list of message packages that can
      be used for sequencing builds of packages.

      @param package_name_list : sort dependencies for these packages only (defaults to all if empty)
      @param package_paths : a python list of ros workspaces (defaults to ROS_PACKAGE_PATH if None is given)
      @return dict mapping relative path to a catkin_pkg.Package
    '''
    if package_paths is None:
        package_paths = os.getenv('ROS_PACKAGE_PATH', '')
        package_paths = [x for x in package_paths.split(':') if x]
    all_packages = {}  # mapping package name to (path, catkin_pkg.Package) tuple
    message_packages = {}
    # use reversed to write over any packages lower down in the overlay heirarchy
    # i.e. no duplicates!
    for path in reversed(package_paths):
        for package_path, package in catkin_pkg.packages.find_packages(path).items():
            # resolve and normalize absolute path because it is used as a key below
            package_path = os.path.normpath(os.path.join(path, package_path))
            all_packages[package.name] = (package_path, package)
            if has_build_depend_on_message_generation(package) or package.name in message_package_whitelist:
                if package_name_list:
                    if package.name in package_name_list:
                        message_packages[package.name] = (package_path, package)
                else:
                    message_packages[package.name] = (package_path, package)
    # put into the correct form for sorting
    # The following returns: A list of tuples containing the relative path and a ``Package`` object,
    sorted_package_tuples = catkin_pkg.topological_order.topological_order_packages(
                                packages=dict(message_packages.values()),
                                whitelisted=None,
                                blacklisted=None,
                                underlay_packages=dict(all_packages.values()))
    # print("%s" % [p.name for (unused_relative_path, p) in sorted_package_tuples])
    return sorted_package_tuples
