#!/usr/bin/env python

##############################################################################
# Imports
##############################################################################

from __future__ import print_function

import os
import sys
import argparse
import subprocess
import shutil
import exceptions

# local imports
import utils
import console

##############################################################################
# Methods
##############################################################################


def parse_arguments():
    argv = sys.argv[1:]
    parser = argparse.ArgumentParser(
        description='Creates a new android package based on catkin and gradle. \n')
    parser.add_argument('name',
                        nargs=1,
                        help='The name for the package')
    parser.add_argument('-t', '--target-version',
                        action='store',
                        default='15',
                        help='Android sdk version [15]')
    parser.add_argument('-p', '--android-package-name',
                        action='store',
                        default='com.github.rosmobile.android.pkg_name',
                        help='Android package name (e.g. com.github.rosmobile.android.pkg_name)')
    parser.add_argument('-a', '--author',
                        action='store',
                        default=utils.author_name(),
                        help='A single author, may be used multiple times')
    args = parser.parse_args(argv)
    if args.android_package_name == "com.github.rosmobile.android.pkg_name":
        args.android_package_name = "com.github.rosmobile.android.%s" % args.name[0].lower()
    return args


def actually_create_android_project(package_name, target_version, java_package_name, is_library):
    path = os.path.join(os.getcwd(), package_name.lower())
    console.pretty_println("\nCreating android project ", console.bold)
    console.pretty_print("  Name      : ", console.cyan)
    console.pretty_println("%s" % package_name, console.yellow)
    console.pretty_print("  Target Ver: ", console.cyan)
    console.pretty_println("%s" % target_version, console.yellow)
    console.pretty_print("  Java Name : ", console.cyan)
    console.pretty_println("%s" % java_package_name, console.yellow)
    if is_library:
        console.pretty_print("  Library   : ", console.cyan)
        console.pretty_println("yes\n", console.yellow)
        cmd = ['android', 'create', 'lib-project', '-n', package_name, '-p', path, '-k', java_package_name, '-t', 'android-' + target_version, ]
    else:
        activity_name = utils.camel_case(package_name)
        console.pretty_print("  Activity  : ", console.cyan)
        console.pretty_println("%s\n" % activity_name, console.yellow)
        cmd = ['android', 'create', 'project', '-n', package_name, '-p', path, '-k', java_package_name, '-t', 'android-' + target_version, '-a', activity_name]
        print("Command: %s" % cmd)
    try:
        subprocess.check_call(cmd)
        print("Command: %s" % cmd)
    except subprocess.CalledProcessError:
        print("Error")
        raise subprocess.CalledProcessError("failed to create android project.")
    except exceptions.OSError as e:
        print("OS error" + str(e))
        raise exceptions.OSError()

    # This is in the old form, let's shovel the shit around to the new form
    utils.mkdir_p(os.path.join(path, 'src', 'main', 'java'))
    os.remove(os.path.join(path, 'local.properties'))
    os.remove(os.path.join(path, 'project.properties'))
    os.remove(os.path.join(path, 'ant.properties'))
    os.remove(os.path.join(path, 'proguard-project.txt'))
    os.remove(os.path.join(path, 'build.xml'))
    os.rmdir(os.path.join(path, 'bin'))
    os.rmdir(os.path.join(path, 'libs'))
    shutil.move(os.path.join(path, 'AndroidManifest.xml'), os.path.join(path, 'src', 'main'))
    shutil.move(os.path.join(path, 'res'), os.path.join(path, 'src', 'main'))
    if not is_library:
        shutil.move(os.path.join(path, 'src', java_package_name.split('.')[0]), os.path.join(path, 'src', 'main', 'java'))

##############################################################################
# Methods acting on classes
##############################################################################


# This inserts the labelled variables into the template wherever the corresponding
# %package, %brief, %description and %depends is found.
def instantiate_template(template, package_name, author, plugin_name, sdk_version):
    return template % locals()


def create_gradle_package_files(args, author, is_library, sdk_version):
    '''
      This is almost a direct copy from catkin_create_pkg.
    '''
    plugin_name = "com.android.library" if is_library else "com.android.application"
    try:
        package_name = args.name[0].lower()
        package_path = os.path.abspath(os.path.join(os.getcwd(), package_name))
        console.pretty_println("\nCreating gradle files", console.bold)
        for template_name in ['build.gradle']:  # 'CMakeLists.txt']:
            filename = os.path.join(package_path, template_name)
            template = read_template_file(template_name)
            contents = instantiate_template(template, package_name, author, plugin_name, sdk_version)
            #if is_library:
            #    contents += extra_gradle_library_text()
            try:
                f = open(filename, 'w')
                f.write(contents)
                console.pretty_print('  File: ', console.cyan)
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
        console.pretty_println("\nIncluding '%s' in the root gradle project configuration (settings.gradle).\n" % name, console.bold)
        settings_gradle.write("include '%s'\n" % name)


def extra_gradle_library_text():
    '''
      Not actually necessary until we start using maven-publish plugin. It doesn't handle dependencies right now.
    '''
    text = "\n"
    text += "/* http://www.flexlabs.org/2013/06/using-local-aar-android-library-packages-in-gradle-builds */\n"
    text += "android.libraryVariants\n"
    text += "publishing {\n"
    text += "    publications {\n"
    text += "        maven(MavenPublication) {\n"
    text += "            /* artifact bundleDebug */\n"
    text += "            artifact bundleRelease\n"
    text += "        }\n"
    text += "    }\n"
    text += "}\n"
    return text


def create_android_project(is_library=False):
    args = parse_arguments()
    actually_create_android_project(args.name[0], args.target_version, args.android_package_name, is_library)
    create_gradle_package_files(args, args.author, is_library, args.target_version)
    add_to_root_gradle_settings(args.name[0])

##############################################################################
# Borrowed from catkin_pkg.package_templates
##############################################################################


def read_template_file(filename):
    template_dir = os.path.join(os.path.dirname(__file__), 'templates', 'android_project')
    template = os.path.join(template_dir, '%s.in' % filename)
    if not os.path.isfile(template):
        raise IOError(
            "Could not read template [%s]" % template
        )
    with open(template, 'r') as fhand:
        template_contents = fhand.read()
    return template_contents
