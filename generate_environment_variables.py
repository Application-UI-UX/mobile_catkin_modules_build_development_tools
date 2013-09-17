#!/usr/bin/env python

import os
import argparse

CATKIN_MARKER_FILE = '.catkin'

def parse_arguments():
    parser = argparse.ArgumentParser(description='Generate environment variables for the rosjava maven environment.')
    cmd_group = parser.add_mutually_exclusive_group()
    cmd_group.add_argument('-d', '--maven-deployment-repository', action='store_true', help='Return the current devel workspace maven directory.')
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
    workspaces = [path for path in paths if os.path.isfile(os.path.join(path, CATKIN_MARKER_FILE))]
    return workspaces

if __name__ == '__main__':
    args = parse_arguments()
    workspaces = get_workspaces(dict(os.environ))
    if args.maven_deployment_repository:
        # assuming one value exists here
        print os.path.join(workspaces[0], 'share', 'maven')
    elif args.maven_path:
        maven_repository_paths = [os.path.join(path, 'share', 'maven') for path in workspaces]
        print os.pathsep.join(maven_repository_paths)
    elif args.gradle_user_home:
        # assuming one value exists here
        print os.path.join(workspaces[0], 'share', 'gradle')
    else:
        print "Nothing to see here - please provide one of the valid command switches."
