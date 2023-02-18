#!/usr/bin/env python

from distutils.core import setup
from catkin_pkg.python_setup import generate_distutils_setup

d = generate_distutils_setup(
    packages=['rosmobile_build_tools'],
    package_dir={'': 'src'},
    scripts=['scripts/catkin_create_android_pkg',
             'scripts/catkin_create_android_project',
             'scripts/catkin_create_android_library_project',
             'scripts/catkin_create_rosmobile_pkg',
             'scripts/catkin_create_rosmobile_project',
             'scripts/catkin_create_rosmobile_library_project',
            ],
    package_data = {'rosmobile_build_tools': [
           'templates/android_package/*',
           'templates/android_project/*',
           'templates/rosmobile_library_project/*',
           'templates/rosmobile_package/*',
           'templates/rosmobile_project/*',
           'templates/init_repo/*',
        ]},
)

setup(**d)
