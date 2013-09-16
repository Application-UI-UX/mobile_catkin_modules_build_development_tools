#!/bin/bash

@[if DEVELSPACE]@
export ROS_MAVEN_PATH=`python @(CMAKE_CURRENT_SOURCE_DIR)/generate_ros_maven_path.py`
export ROS_MAVEN_DEPLOYMENT_PATH=`python @(CMAKE_CURRENT_SOURCE_DIR)/generate_ros_maven_path.py --deployment-repository`
mkdir -p @(CATKIN_DEVEL_PREFIX)/share/gradle
export GRADLE_USER_HOME=@(CATKIN_DEVEL_PREFIX)/share/gradle
@[else]@
export ROS_MAVEN_PATH=`python @(CMAKE_INSTALL_PREFIX)/share/rosjava_build_tools/generate_ros_maven_path.py`
export ROS_MAVEN_DEPLOYMENT_PATH=`python @(CMAKE_INSTALL_PREFIX)/share/rosjava_build_tools/generate_ros_maven_path.py --deployment-repository`
@[end if]@


