#!/usr/bin/env python

from distutils.core import setup
from catkin_pkg.python_setup import generate_distutils_setup

d = generate_distutils_setup(
    packages=['rosjava_tools'],
    package_dir={'': 'src'},
    scripts=['scripts/catkin_create_android_repo',
             'scripts/catkin_create_android_pkg',
             'scripts/catkin_create_android_library_pkg'
            ],
    package_data = {'rosjava_tools': [
           'gradle/gradlew',
           'gradle/gradle/wrapper/*'
           'templates/android_package/*',
           'templates/init_repo/*',
        ]},
    requires=['rospy' 'rospkg']
)

setup(**d)
