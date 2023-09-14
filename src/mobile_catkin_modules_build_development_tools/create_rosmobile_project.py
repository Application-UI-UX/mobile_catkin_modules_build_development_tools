#!/usr/bin/env python

##############################################################################
# Imports
##############################################################################

from __future__ import print_function

import os
import re
import sys
import argparse
import xml.etree.ElementTree as ElementTree

# local imports
import utils
import console

##############################################################################
# Methods
##############################################################################


def parse_arguments():
    argv = sys.argv[1:]
    parser = argparse.ArgumentParser(
        description='Creates a new rosmobile package based on catkin and gradle. \n')
    parser.add_argument('name',
                        nargs=1,
                        help='The name for the package')
    parser.add_argument('-a', '--author',
                        action='store',
                        default=utils.author_name(),
                        help='A single author, may be used multiple times')
    args = parser.parse_args(argv)
    return args


##############################################################################
# Methods acting on classes
##############################################################################


# This inserts the labelled variables into the template wherever the corresponding
# %package, %brief, %description and %depends is found.
def instantiate_template(template, project_name, author):
    return template % locals()


def instantiate_code_template(template, package_name, project_name, author):
    return template % locals()


def create_gradle_package_files(args, template_directory):
    '''
      This is almost a direct copy from catkin_create_pkg.
    '''
    try:
        project_name = args.name[0].lower()
        package_path = os.path.abspath(os.path.join(os.getcwd(), project_name))
        for template_name in ['build.gradle']:  # 'CMakeLists.txt']:
            filename = os.path.join(package_path, template_name)
            template = utils.read_template_file(template_directory, template_name)
            contents = instantiate_template(template, project_name, args.author)
            try:
                f = open(filename, 'w')
                f.write(contents)
                console.pretty_print('  File      : ', console.cyan)
                console.pretty_println(template_name, console.yellow)
            finally:
                f.close()
    except Exception:
        raise


def create_talker_listener_classes(project_name, template_directory, author):
    path = os.path.join(os.getcwd(), project_name.lower())
    package_name = os.path.basename(os.getcwd())
    java_package_path = os.path.join(path, 'src', 'main', 'java', 'com', 'github', package_name, project_name)
    utils.mkdir_p(java_package_path)
    try:
        for template_name in ['Talker.java', 'Listener.java']:
            filename = os.path.join(java_package_path, template_name)
            template = utils.read_template_file(template_directory, template_name)
            contents = instantiate_code_template(template, package_name, project_name, author)
            try:
                f = open(filename, 'w')
                f.write(contents)
                console.pretty_print('  File      : ', console.cyan)
                console.pretty_println(template_name, console.yellow)
            finally:
                f.close()
    except Exception:
        raise


def add_to_root_gradle_settings(name):
    '''
      Adds project name to the root level settings.gradle file.
    '''
    for rel_path in ['.', '..']:
        settings_gradle_path = os.path.join(os.getcwd(), rel_path, 'settings.gradle')
        if os.path.isfile(settings_gradle_path):
            break
        else:
            settings_gradle_path = None
    if settings_gradle_path is None:
        console.pretty_println("\nCouldn't find the root level settings.gradle file - not adding to the superproject.")
        return
    with open(settings_gradle_path, 'a') as settings_gradle:
        console.pretty_print('  File      : ', console.cyan)
        console.pretty_println('settings.gradle', console.yellow)
        settings_gradle.write("include '%s'\n" % name)


def add_catkin_generate_tree_command():
    for rel_path in ['.', '..']:
        build_gradle_path = os.path.join(os.getcwd(), rel_path, 'build.gradle')
        if os.path.isfile(build_gradle_path):
            break
        else:
            build_gradle_path = None
    if build_gradle_path is None:
        console.pretty_println("\nCouldn't find the root level build.gradle file - not adding to the superproject.")
        return
    with open(build_gradle_path, 'r') as build_gradle:
        console.pretty_print('  File      : ', console.cyan)
        console.pretty_println('build.gradle (catkin_generate_tree update)', console.yellow)
        new_contents = build_gradle.read().replace("apply plugin: 'catkin'", "apply plugin: 'catkin'\nproject.catkin.tree.generate()\n")
    with open(build_gradle_path, 'w') as build_gradle:
        build_gradle.write(new_contents)


def add_to_package_xml(name):
    '''
      Adds project name to build_depends in package.xml (should be same name as the ros msg package name).
    '''
    for rel_path in ['.', '..']:
        package_xml_path = os.path.join(os.getcwd(), rel_path, 'package.xml')
        if os.path.isfile(package_xml_path):
            break
        else:
            package_xml_path = None
    if package_xml_path is None:
        console.pretty_println("\nCouldn't find the root level package.xml file - not adding to the superproject.")
        return
    with open(package_xml_path, 'r') as package_xml:
        console.pretty_print('  File      : ', console.cyan)
        console.pretty_println('package.xml (dependency update)', console.yellow)
        new_contents = package_xml.read().replace("</package>", "<build_depend>%s</build_depend>\n</package>" % name)
    with open(package_xml_path, 'w') as package_xml:
        package_xml.write(new_contents)


def add_tasks_to_cmake_setup(tasks):
    '''
      Adds project name to build_depends in package.xml (should be same name as the ros msg package name).
    '''
    for rel_path in ['.', '..']:
        cmakelists_txt_path = os.path.join(os.getcwd(), rel_path, 'CMakeLists.txt')
        if os.path.isfile(cmakelists_txt_path):
            break
        else:
            cmakelists_txt_path = None
    if cmakelists_txt_path is None:
        console.pretty_println("\nCouldn't find the root level CMakeLists.txt - not adding to the superproject.")
        return
    with open(cmakelists_txt_path, 'r') as cmakelists_txt:
        old_contents = cmakelists_txt.read()
        result = re.search('^catkin_rosmobile_setup\(.*\)', old_contents, re.MULTILINE)
        if result is None:
            console.pretty_println("\nCouldn't find a catkin_rosmobile_setup entry in the CMakeLists.txt - not adding tasks.")
            return
        rosmobile_setup_string = result.group(0)
        gradle_tasks = set([])
        if rosmobile_setup_string.find("publish") == -1:
            gradle_tasks.add("publish")
        if rosmobile_setup_string.find("installDist") == -1:
            gradle_tasks.add("installDist")
        gradle_tasks |= set(tasks)
        console.pretty_print('  File      : ', console.cyan)
        console.pretty_println('CMakeLists.txt (gradle task update)', console.yellow)
        old_text = rosmobile_setup_string
        new_text = 'catkin_rosmobile_setup(' + ' '.join(gradle_tasks) + ')'
        new_contents = old_contents.replace(old_text, new_text)
    with open(cmakelists_txt_path, 'w') as cmakelists_txt:
        cmakelists_txt.write(new_contents)


def create_dummy_java_class(project_name):
    path = os.path.join(os.getcwd(), project_name.lower())
    package_name = os.path.basename(os.getcwd())
    java_package_path = os.path.join(path, 'src', 'main', 'java', 'com', 'github', package_name, project_name)
    utils.mkdir_p(java_package_path)
    filename = os.path.join(java_package_path, 'Dude.java')
    java_class = "package com.github.%s.%s;\n" % (package_name, project_name)
    java_class += "\n"
    java_class += "public class Dude {\n"
    java_class += "}\n"
    console.pretty_print('  File      : ', console.cyan)
    console.pretty_println('Dude.class', console.yellow)
    with open(filename, 'w') as dude_class:
        dude_class.write(java_class)


def ros_package_name():
    for rel_path in ['.', '..']:
        package_xml_path = os.path.join(os.getcwd(), rel_path, 'package.xml')
        if os.path.isfile(package_xml_path):
            break
        else:
            package_xml_path = None
    if package_xml_path is None:
        console.pretty_println("\nCouldn't find the root level package.xml file - not adding to the superproject.")
        return
    tree = ElementTree.parse(package_xml_path)
    root = tree.getroot()
    name = root.find('name').text
    return name


def create_rosmobile_project_common(args, template_directory):
    project_name = args.name[0]
    console.pretty_println("\nCreating rosmobile project ", console.bold)
    console.pretty_print("  Name      : ", console.cyan)
    console.pretty_println("%s" % project_name, console.yellow)
    utils.mkdir_p(os.path.join(os.getcwd(), project_name.lower()))
    # This is in the old form, let's shovel the shit around to the new form
    create_gradle_package_files(args, template_directory)
    add_to_root_gradle_settings(args.name[0])


def create_rosmobile_project():
    args = parse_arguments()
    project_name = args.name[0]
    author = args.author
    create_rosmobile_project_common(args, 'rosmobile_project')
    create_talker_listener_classes(project_name, 'rosmobile_project', author)
    add_tasks_to_cmake_setup(['installDist', 'publish'])


def create_rosmobile_library_project():
    args = parse_arguments()
    project_name = args.name[0]
    create_rosmobile_project_common(args, 'rosmobile_library_project')
    create_dummy_java_class(project_name)
    add_tasks_to_cmake_setup(['publish'])


def create_rosmobile_msg_project():
    args = parse_arguments()
    project_name = args.name[0]
    create_rosmobile_project_common(args, 'rosmobile_msg_project')
    add_catkin_generate_tree_command()
    add_to_package_xml(project_name)
    add_tasks_to_cmake_setup(['publish'])
