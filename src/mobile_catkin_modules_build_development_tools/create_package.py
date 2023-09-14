#!/usr/bin/env python

##############################################################################
# Imports
##############################################################################

import os
import sys
import argparse
import subprocess
import catkin_pkg
from catkin_pkg.package_templates import create_package_xml, PackageTemplate

# local imports
import utils
import console

##############################################################################
# Methods
##############################################################################


def parse_arguments():
    argv = sys.argv[1:]
    parser = argparse.ArgumentParser(
        description='Creates a new rosmobile/android repository based on catkin and gradle. \n\nNote that the path you provide will become the maven group for your repo.\n')
    parser.add_argument('path', nargs='?', default=os.getcwd(), help='path to the repository you wish to create (must not exist beforehand).')
    parser.add_argument('dependencies',
                        nargs='*',
                        help='Dependency list')
    parser.add_argument('-l', '--license',
                        action='append',
                        default=["Apache 2.0"],
                        help='Name for License, (e.g. BSD, MIT, GPLv3...)[BSD]')
    parser.add_argument('-a', '--author',
                        action='append',
                        help='A single author, may be used multiple times')
    parser.add_argument('-m', '--maintainer',
                        action='append',
                        help='A single maintainer, may be used multiple times')
    parser.add_argument('-V', '--pkg_version',
                        action='store',
                        default="0.1.0",
                        help='Initial Package version [0.1.0]')
    parser.add_argument('-D', '--description',
                        action='store',
                        help='Description')
    args = parser.parse_args(argv)
#    if not args.author:
#        args.author = []
#        args.author.append(utils.author_name)
#    if not args.maintainer:
#        args.maintainer = []
#        args.maintainer.append(catkin_pkg.package.Person(utils.author_name))
#    else:
#        args.maintainer = []
#        args.maintainer.append(catkin_pkg.package.Person(utils.author_name))
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


def get_templates(template_directory):
    template_dir = os.path.join(os.path.dirname(__file__), 'templates', template_directory)
    templates = {}
    templates['CMakeLists.txt'] = read_template(os.path.join(template_dir, 'CMakeLists.txt.in'))
    templates['build.gradle'] = read_template(os.path.join(template_dir, 'build.gradle.in'))
    templates['settings.gradle'] = read_template(os.path.join(template_dir, 'settings.gradle'))
    return templates


def populate_repo(repo_path, package_type):
    author = utils.author_name()
    repo_name = os.path.basename(repo_path)
    templates = get_templates(package_type)
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


def create_catkin_package_files(package_name, package_path, args):
    '''
      This is almost a direct copy from catkin_create_pkg.
    '''
    try:
        build_depends = []
        if 'mobile_catkin_modules_build_development_tools' not in args.dependencies:
            build_depends.append(catkin_pkg.package.Dependency('mobile_catkin_modules_build_development_tools'))
        for depend_name in args.dependencies:
            build_depends.append(catkin_pkg.package.Dependency(depend_name))
        package_template = PackageTemplate._create_package_template(
            package_name=package_name,
            description=args.description,
            licenses=args.license or [],
            maintainer_names=args.maintainer,
            author_names=args.author,
            version=args.pkg_version,
            catkin_deps=[],
            system_deps=[],
            boost_comps=None)
        package_template.exports = []
        package_template.build_depends = build_depends
        distro_version = utils.distro_version()
        package_xml = create_package_xml(package_template=package_template, rosdistro=distro_version)
        try:
            filename = os.path.join(package_path, 'package.xml')
            f = open(filename, 'w')
            f.write(package_xml)
            console.pretty_print('Created repo file: ', console.cyan)
            console.pretty_println('%s' % filename, console.yellow)
        finally:
            f.close()
    except Exception:
        raise

##############################################################################
# Methods acting on classes
##############################################################################


def init_package(package_type):
    args = parse_arguments()
    try:
        repo_path = utils.validate_path(args.path)
        repo_name = os.path.basename(os.path.normpath(repo_path)).lower()
        populate_repo(repo_path, package_type)
        create_catkin_package_files(repo_name, repo_path, args)
        create_gradle_wrapper(repo_path)
    except Exception:
        raise


def init_rosmobile_package():
    init_package('rosmobile_package')


def init_android_package():
    init_package('android_package')
