##############################################################################
# CMake
##############################################################################

cmake_minimum_required(VERSION 3.5)
project(mobile_catkin_modules_build_development_tools)

##############################################################################
# Catkin
##############################################################################

# Find ROS
if($ENV{ROS_VERSION} EQUAL 1)
  find_package(catkin REQUIRED)
else()
  find_package(ament_cmake REQUIRED)
endif()

find_package(catkin REQUIRED)
# catkin_package(CFG_EXTRAS rosmobile.cmake)

catkin_python_setup()
catkin_add_env_hooks(15.rosmobile SHELLS bash DIRECTORY ${CMAKE_CURRENT_SOURCE_DIR}/env-hooks)
catkin_add_env_hooks(15.rosmobile SHELLS sh DIRECTORY ${CMAKE_CURRENT_SOURCE_DIR}/env-hooks)

##############################################################################
# Project Settings
##############################################################################

# Have to install gradle here so we can retain executable permissions
# If we do via setup.py with the data subsection, it loses permissions
install(
  PROGRAMS src/mobile_catkin_modules_build_development_tools/gradle/gradlew
  DESTINATION ${CATKIN_PACKAGE_PYTHON_DESTINATION}/gradle
)

install(
  DIRECTORY src/mobile_catkin_modules_build_development_tools/gradle/gradle
  DESTINATION ${CATKIN_PACKAGE_PYTHON_DESTINATION}/gradle
)

install(
  PROGRAMS generate_environment_variables.py
  DESTINATION ${CATKIN_PACKAGE_SHARE_DESTINATION}/python
)

install(
  FILES LICENSE
  DESTINATION ${CATKIN_PACKAGE_SHARE_DESTINATION}/python
)
