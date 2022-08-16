#!/bin/sh

@[if DEVELSPACE]@
SCRIPT=@(CMAKE_CURRENT_SOURCE_DIR)/generate_environment_variables.py
@[else]@
SCRIPT=@(CMAKE_INSTALL_PREFIX)/share/rosjava_build_tools/generate_environment_variables.py
@[end if]@

export ROS_MAVEN_PATH="`python ${SCRIPT} --maven-path`"
export ROS_MAVEN_DEPLOYMENT_REPOSITORY="`python ${SCRIPT} --maven-deployment-repository`"
export ROS_MAVEN_REPOSITORY="`python ${SCRIPT} --maven-repository`"
