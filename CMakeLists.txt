##############################################################################
# CMake
##############################################################################

cmake_minimum_required(VERSION 2.8.3)
project(rosjava_tools)

##############################################################################
# Catkin
##############################################################################

find_package(catkin REQUIRED)
catkin_package(CFG_EXTRAS rosjava.cmake)

catkin_python_setup()

##############################################################################
# Project Settings
##############################################################################

# Graveyarded for now
#install(
#    PROGRAMS 
#        scripts/android_post_build_script
#    DESTINATION ${CATKIN_PACKAGE_BIN_DESTINATION}
#    )

#install(DIRECTORY launch
#  DESTINATION ${CATKIN_PACKAGE_SHARE_DESTINATION})
#
#install(DIRECTORY param
#  DESTINATION ${CATKIN_PACKAGE_SHARE_DESTINATION})

