#!/bin/sh

@[if DEVELSPACE]@
export ROS_MAVEN_PATH=`python @(CMAKE_CURRENT_SOURCE_DIR)/generate_environment_variables.py --maven-path`
export ROS_MAVEN_DEPLOYMENT_PATH=`python @(CMAKE_CURRENT_SOURCE_DIR)/generate_environment_variables.py --maven-deployment-repository`
export GRADLE_USER_HOME=`python @(CMAKE_CURRENT_SOURCE_DIR)/generate_environment_variables.py --gradle-user-home`
mkdir -p ${GRADLE_USER_HOME}
@[else]@
export ROS_MAVEN_PATH=`python @(CMAKE_INSTALL_PREFIX)/share/rosjava_build_tools/generate_environment_variables.py --maven-path`
export ROS_MAVEN_DEPLOYMENT_PATH=`python @(CMAKE_INSTALL_PREFIX)/share/rosjava_build_tools/generate_environment_variables.py --maven-deployment-repository`
@[end if]@
