#!/bin/bash

@[if DEVELSPACE]@
SCRIPT=@(CMAKE_CURRENT_SOURCE_DIR)/generate_environment_variables.py
@[else]@
SCRIPT=@(CMAKE_INSTALL_PREFIX)/share/rosjava_build_tools/generate_environment_variables.py
@[end if]@

# Conditionally set these variables - i.e. if the user wants to override them, that is ok.
: ${ROS_MAVEN_PATH:=`python ${SCRIPT} --maven-path`}
: ${ROS_MAVEN_DEPLOYMENT_REPOSITORY:=`python ${SCRIPT} --maven-deployment-repository`}
: ${GRADLE_USER_HOME:=`python ${SCRIPT} --gradle-user-home`}
export ROS_MAVEN_PATH
export ROS_MAVEN_DEPLOYMENT_REPOSITORY
export GRADLE_USER_HOME

#export ROS_MAVEN_PATH=`python @(CMAKE_CURRENT_SOURCE_DIR)/generate_environment_variables.py --maven-path`
#export ROS_MAVEN_DEPLOYMENT_REPOSITORY=`python @(CMAKE_CURRENT_SOURCE_DIR)/generate_environment_variables.py --maven-deployment-repository`
#export GRADLE_USER_HOME=`python @(CMAKE_CURRENT_SOURCE_DIR)/generate_environment_variables.py --gradle-user-home`
