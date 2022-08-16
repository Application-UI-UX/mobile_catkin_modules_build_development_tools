#!/usr/bin/env python

from distutils.core import setup
from catkin_pkg.python_setup import generate_distutils_setup

d = generate_distutils_setup(
    packages=['rosjava_build_tools'],
    package_dir={'': 'src'},
    scripts=['scripts/catkin_create_android_pkg',
             'scripts/catkin_create_android_project',
             'scripts/catkin_create_android_library_project',
             'scripts/catkin_create_rosjava_pkg',
             'scripts/catkin_create_rosjava_project',
             'scripts/catkin_create_rosjava_library_project',
            ],
    package_data = {'rosjava_build_tools': [
           'templates/android_package/*',
           'templates/android_project/*',
           'templates/rosjava_library_project/*',
           'templates/rosjava_package/*',
           'templates/rosjava_project/*',
           'templates/init_repo/*',
        ]},
)

setup(**d)
