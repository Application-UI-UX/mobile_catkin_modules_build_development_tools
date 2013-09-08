#!/bin/bash

@[if DEVELSPACE]@
export ROS_MAVEN_PATH=`python @(CMAKE_CURRENT_SOURCE_DIR)/generate_ros_maven_path.py`
export ROS_MAVEN_DEPLOYMENT_PATH=`python @(CMAKE_CURRENT_SOURCE_DIR)/generate_ros_maven_path.py --deployment-repository`
@[else]@
export ROS_MAVEN_PATH=`python @(CMAKE_INSTALL_PREFIX)/share/rosjava_build_tools/generate_ros_maven_path.py`
@[end if]@


