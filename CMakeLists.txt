##############################################################################
# CMake
##############################################################################

cmake_minimum_required(VERSION 2.8.3)
project(rosjava_build_tools)

##############################################################################
# Catkin
##############################################################################

find_package(catkin REQUIRED)
catkin_package(CFG_EXTRAS rosjava.cmake)

catkin_python_setup()
catkin_add_env_hooks(15.rosjava SHELLS bash DIRECTORY ${CMAKE_CURRENT_SOURCE_DIR}/env-hooks)
catkin_add_env_hooks(15.rosjava SHELLS sh DIRECTORY ${CMAKE_CURRENT_SOURCE_DIR}/env-hooks)

##############################################################################
# Project Settings
##############################################################################

# Have to install gradle here so we can retain executable permissions
# If we do via setup.py with the data subsection, it loses permissions
install(
    PROGRAMS src/rosjava_build_tools/gradle/gradlew
    DESTINATION ${CATKIN_PACKAGE_PYTHON_DESTINATION}/gradle
    )

install(
    DIRECTORY src/rosjava_build_tools/gradle/gradle
    DESTINATION ${CATKIN_PACKAGE_PYTHON_DESTINATION}/gradle
  )

install(
    PROGRAMS generate_environment_variables.py
    DESTINATION ${CATKIN_PACKAGE_SHARE_DESTINATION}
    )

install(
    FILES LICENSE
    DESTINATION ${CATKIN_PACKAGE_SHARE_DESTINATION}
    )

set(ROS_MAVEN_DEPLOYMENT_REPOSITORY $ENV{ROS_MAVEN_DEPLOYMENT_REPOSITORY})
if(NOT ROS_MAVEN_DEPLOYMENT_REPOSITORY)
    set(ROS_MAVEN_DEPLOYMENT_REPOSITORY "${CATKIN_DEVEL_PREFIX}/${CATKIN_GLOBAL_SHARE_DESTINATION}/maven")
endif()
file(WRITE ${ROS_MAVEN_DEPLOYMENT_REPOSITORY}/rospack_nosubdirs "")
install(FILES ${ROS_MAVEN_DEPLOYMENT_REPOSITORY}/rospack_nosubdirs
        DESTINATION ${CATKIN_GLOBAL_SHARE_DESTINATION}/maven)
