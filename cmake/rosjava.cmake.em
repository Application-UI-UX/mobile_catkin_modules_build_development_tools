##############################################################################
# Utilities
##############################################################################

# Scans down directories till it finds the gradle wrapper.
# It sets the following variables
# - ${PROJECT_NAME}_gradle_BINARY
macro(find_gradle)
    find_file(${PROJECT_NAME}_gradle_BINARY gradlew
          PATHS 
          ${CMAKE_CURRENT_SOURCE_DIR}
          ${CMAKE_CURRENT_SOURCE_DIR}/..
          ${CMAKE_CURRENT_SOURCE_DIR}/../..
          NO_DEFAULT_PATH
          )
     if(NOT ${PROJECT_NAME}_gradle_BINARY)
         message(FATAL_ERROR "Could not find the gradle wrapper in this directory or below.")
     endif()
endmacro()

# Scans down directories till it finds the gradle project settings. 
# It sets the following variables
# - ${PROJECT_NAME}_gradle_ROOT
macro(find_gradle_repo_root)
    find_file(${PROJECT_NAME}_gradle_SETTINGS settings.gradle
          PATHS 
          ${CMAKE_CURRENT_SOURCE_DIR}
          ${CMAKE_CURRENT_SOURCE_DIR}/..
          ${CMAKE_CURRENT_SOURCE_DIR}/../..
          NO_DEFAULT_PATH
          )
     if(NOT ${PROJECT_NAME}_gradle_SETTINGS)
         message(FATAL_ERROR "Could not find the settings.gradle file in this directory or below.")
     endif()
     get_filename_component(${PROJECT_NAME}_gradle_ROOT ${${PROJECT_NAME}_gradle_SETTINGS} PATH)
endmacro()

##############################################################################
# RosJava Package
##############################################################################
# Calls the gradle wrapper to compile just the package
# that it is called in with install and installApp targets.
macro(catkin_rosjava_setup)
    find_gradle()
    add_custom_target(gradle-${PROJECT_NAME}
        ALL
        COMMAND ${CATKIN_ENV} ${${PROJECT_NAME}_gradle_BINARY} install installApp 
        WORKING_DIRECTORY ${CMAKE_CURRENT_SOURCE_DIR}
    )
    catkin_package_xml()
    foreach(depends in ${${PROJECT_NAME}_BUILD_DEPENDS})
        if(TARGET gradle-${depends})
            #message(STATUS "Adding dependency gradle-${depends}")
            add_dependencies(gradle-${PROJECT_NAME} gradle-${depends})
        endif()
    endforeach()
    if(NOT TARGET gradle-clean)
        add_custom_target(gradle-clean)
    endif()
    add_custom_target(gradle-clean-${PROJECT_NAME}
        COMMAND ${CATKIN_ENV} ${${PROJECT_NAME}_gradle_BINARY} clean
        WORKING_DIRECTORY ${CMAKE_CURRENT_SOURCE_DIR}
    )
    add_dependencies(gradle-clean gradle-clean-${PROJECT_NAME})
endmacro()

##############################################################################
# RosJava Repo
##############################################################################

# Calls the root level gradle wrapper to run the multi-project 
# configuration and compile the entire suite.
macro(catkin_rosjava_repo_setup)
    find_gradle()
    find_gradle_repo_root()
    add_custom_target(gradle-${PROJECT_NAME}
        ALL
        COMMAND ${CATKIN_ENV} ${${PROJECT_NAME}_gradle_BINARY} install installApp 
        WORKING_DIRECTORY ${${PROJECT_NAME}_gradle_ROOT}
    )
    catkin_package_xml()
    foreach(depends in ${${PROJECT_NAME}_BUILD_DEPENDS})
        if(TARGET gradle-${depends})
            #message(STATUS "Adding dependency gradle-${depends}")
            add_dependencies(gradle-${PROJECT_NAME} gradle-${depends})
        endif()
    endforeach()
endmacro()

##############################################################################
# Android Package
##############################################################################
# Calls the gradle wrapper to compile the android package.
# It checks the build type and determines whether it should run
# assembleDebug or assembleRelease
macro(catkin_android_setup)
    find_gradle()
    if(CMAKE_BUILD_TYPE STREQUAL "Release")
      set(gradle_task "assembleRelase")
    else()
      set(gradle_task "assembleDebug")
    endif()
    add_custom_target(gradle-${PROJECT_NAME}
        ALL
        COMMAND ${CATKIN_ENV} ${${PROJECT_NAME}_gradle_BINARY} ${gradle_task} install
        WORKING_DIRECTORY ${CMAKE_CURRENT_SOURCE_DIR}
    )
    catkin_package_xml()
    foreach(depends in ${${PROJECT_NAME}_BUILD_DEPENDS})
        if(TARGET gradle-${depends})
            #message(STATUS "Adding dependency gradle-${depends}")
            add_dependencies(gradle-${PROJECT_NAME} gradle-${depends})
        endif()
    endforeach()
    if(NOT TARGET gradle-clean)
        add_custom_target(gradle-clean)
    endif()
    add_custom_target(gradle-clean-${PROJECT_NAME}
        COMMAND ${CATKIN_ENV} ${${PROJECT_NAME}_gradle_BINARY} clean
        WORKING_DIRECTORY ${CMAKE_CURRENT_SOURCE_DIR}
    )
    add_dependencies(gradle-clean gradle-clean-${PROJECT_NAME})
endmacro()

