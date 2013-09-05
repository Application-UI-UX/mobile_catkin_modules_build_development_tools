#!/bin/bash

@[if DEVELSPACE]@
export ROS_MAVEN_PATH=`python @(CMAKE_CURRENT_SOURCE_DIR)/generate_ros_maven_path.py`
@[else]@
export ROS_MAVEN_PATH=`python @(CMAKE_INSTALL_PREFIX)/share/rosjava_tools/generate_ros_maven_path.py`
@[end if]@


