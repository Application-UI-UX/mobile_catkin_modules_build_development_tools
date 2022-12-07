#!/usr/bin/env python

import os
import argparse

CATKIN_MARKER_FILE = '.catkin'

def parse_arguments():
    parser = argparse.ArgumentParser(description='Generate environment variables for the rosmobile maven environment.')
    cmd_group = parser.add_mutually_exclusive_group()
    cmd_group.add_argument('-d', '--maven-deployment-repository', action='store_true', help='Return the current devel workspace maven directory.')
    cmd_group.add_argument('-r', '--maven-repository', action='store_true', help='The url to the external ros maven repository.')
    cmd_group.add_argument('-m', '--maven-path', action='store_true', help='Generate maven path across all chained workspcaes.')
    cmd_group.add_argument('-g', '--gradle-user-home', action='store_true', help='Generate the local gradle user home in the current devel workspace (share/gradle).')
    args = parser.parse_args()
    return args

def get_workspaces(environ):
    '''
    Based on CMAKE_PREFIX_PATH return all catkin workspaces.
    '''
    # get all cmake prefix paths
    env_name = 'CMAKE_PREFIX_PATH'
    value = environ[env_name] if env_name in environ else ''
    paths = [path for path in value.split(os.pathsep) if path]
    # remove non-workspace paths
    workspaces = [path.replace(' ', '\ ') for path in paths if os.path.isfile(os.path.join(path, CATKIN_MARKER_FILE))]
    return workspaces

def get_environment_variable(environ, key):
    var = None
    try:
        var = environ[key]
    except KeyError:
        pass
    if var == '':
        var = None
    return var

if __name__ == '__main__':
    args = parse_arguments()
    environment_variables = dict(os.environ)
    workspaces = get_workspaces(environment_variables)
    if args.maven_deployment_repository:
        repo = get_environment_variable(environment_variables, 'ROS_MAVEN_DEPLOYMENT_REPOSITORY')
        if repo is None:
            repo = os.path.join(workspaces[0], 'share', 'maven')
        else:
            if repo in [os.path.join(w, 'share', 'maven') for w in workspaces]:
                repo = os.path.join(workspaces[0], 'share', 'maven')
        print(repo)
    elif args.maven_path:
        new_maven_paths = [os.path.join(path, 'share', 'maven') for path in workspaces]
        maven_paths = get_environment_variable(environment_variables, 'ROS_MAVEN_PATH')
        if maven_paths is None:
            maven_paths = new_maven_paths
        else:
            maven_paths = maven_paths.split(os.pathsep)
            common_paths = [p for p in maven_paths if p in new_maven_paths]
            if common_paths:
                maven_paths = new_maven_paths
        print(os.pathsep.join(maven_paths))
    elif args.gradle_user_home:
        home = get_environment_variable(environment_variables, 'GRADLE_USER_HOME')
        if home is None:
            home = os.path.join(workspaces[0], 'share', 'gradle')
        else:
            if home in [os.path.join(w, 'share', 'gradle') for w in workspaces]:
                home = os.path.join(workspaces[0], 'share', 'gradle')
        print(home)
    else:
        print("Nothing to see here - please provide one of the valid command switches.")
