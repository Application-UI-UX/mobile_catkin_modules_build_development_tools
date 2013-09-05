#!/usr/bin/env python

import os

CATKIN_MARKER_FILE = '.catkin'

def get_workspaces(environ):
    '''
    Based on CMAKE_PREFIX_PATH return all catkin workspaces.
    '''
    # get all cmake prefix paths
    env_name = 'CMAKE_PREFIX_PATH'
    value = environ[env_name] if env_name in environ else ''
    paths = [path for path in value.split(os.pathsep) if path]
    # remove non-workspace paths
    workspaces = [path for path in paths if os.path.isfile(os.path.join(path, CATKIN_MARKER_FILE)) or (include_fuerte and path.startswith('/opt/ros/fuerte'))]
    return workspaces

if __name__ == '__main__':
    workspaces = get_workspaces(dict(os.environ))
    maven_repository_paths = [os.path.join(path, 'maven') for path in workspaces]
    print os.pathsep.join(maven_repository_paths)
