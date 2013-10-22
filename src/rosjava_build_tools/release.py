#!/usr/bin/env python

##############################################################################
# Imports
##############################################################################

from rosinstall_generator.generator import ARG_ALL_PACKAGES, generate_rosinstall, sort_rosinstall

##############################################################################
# Imports
##############################################################################


def scrape_for_release_message_packages(track):
    try:
        # Should use ROS_DISTRO here, or some passed in value.
        rosinstall_data = generate_rosinstall(track, [ARG_ALL_PACKAGES],
            wet_only=True, dry_only=False
            )
    except RuntimeError as unused_e:
        raise RuntimeError("error occured while scraping rosdistro for msg package naems and versions.")
    rosinstall_data = sort_rosinstall(rosinstall_data)
    #print("%s" % rosinstall_data)
    packages = []
    for element in rosinstall_data:
        for unused_key, value in element.items():
            if "_msgs" in value['local-name'] or "_srvs" in value['local-name']:
                name = value['local-name']
                # bloom version is usually of the form: 'release/hydro/zeroconf_msgs/0.2.1-0'
                version = value['version'].split('/')[-1].split('-')[0]
                pkg = {'name': name, 'version': version}
                packages.append(pkg)
    return packages
