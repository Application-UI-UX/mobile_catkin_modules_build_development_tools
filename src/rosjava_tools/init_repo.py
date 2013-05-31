#!/usr/bin/env python
#
# License: Apache 2.0
#   https://raw.github.com/ros-java/rosjava_core/hydro-devel/rocon_tools/LICENSE
#

##############################################################################
# Imports
##############################################################################

import os
import sys
import argparse
import subprocess

# local imports
import utils
import console

##############################################################################
# Methods
##############################################################################


def parse_arguments():
    argv = sys.argv[1:]
    parser = argparse.ArgumentParser(
        description='Creates a new android repository based on catkin and gradle. \n\nNote that the path you provide will become the maven group for your repo.\n')
    parser.add_argument('path', nargs='?', default=os.getcwd(), help='path to the repository you wish to create (must not exist beforehand).')
    args = parser.parse_args(argv)
    return args


# Finds and reads one of the templates.
def read_template(tmplf):
    f = open(tmplf, 'r')
    try:
        t = f.read()
    finally:
        f.close()
    return t


# This inserts the labelled variables into the template wherever the corresponding
# %package, %brief, %description and %depends is found.
def instantiate_template(template, repo_name, author):
    return template % locals()


def get_templates():
    template_dir = os.path.join(os.path.dirname(__file__), 'templates', 'init_repo')
    templates = {}
    templates['build.gradle'] = read_template(os.path.join(template_dir, 'build.gradle.in'))
    templates['settings.gradle'] = read_template(os.path.join(template_dir, 'settings.gradle'))
    return templates


def populate_repo(repo_path):
    author = utils.author_name()
    repo_name = os.path.basename(repo_path)
    templates = get_templates()
    for filename, template in templates.iteritems():
        contents = instantiate_template(template, repo_name, author)
        try:
            p = os.path.abspath(os.path.join(repo_path, filename))
            f = open(p, 'w')
            f.write(contents)
            console.pretty_print("Created repo file: ", console.cyan)
            console.pretty_println("%s" % p, console.yellow)
        finally:
            f.close()


def create_gradle_wrapper(repo_path):
    gradle_binary = os.path.join(os.path.dirname(__file__), 'gradle', 'gradlew')
    cmd = [gradle_binary, '-p', repo_path, 'wrapper']
    console.pretty_print("Creating gradle wrapper: ", console.cyan)
    console.pretty_println("%s" % ' '.join(cmd), console.yellow)
    try:
        subprocess.check_call(cmd)
    except subprocess.CalledProcessError:
        raise subprocess.CalledProcessError("failed to create the gradle wrapper.")

##############################################################################
# Methods acting on classes
##############################################################################


def init_android_repo():
    args = parse_arguments()
    try:
        repo_path = utils.validate_path(args.path)
        populate_repo(repo_path)
        create_gradle_wrapper(repo_path)
    except Exception:
        raise
