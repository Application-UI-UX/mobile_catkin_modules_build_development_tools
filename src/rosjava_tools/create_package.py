#!/usr/bin/env python
#
# License: Apache 2.0
#   https://raw.github.com/ros-java/rosjava_core/hydro-devel/rocon_tools/LICENSE
#

##############################################################################
# Imports
##############################################################################

from __future__ import print_function

import os
import sys
import argparse
import subprocess
import shutil

# local imports
import utils
import console
import catkin_pkg
from catkin_pkg.package_templates import create_package_xml, PackageTemplate

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
    parser.add_argument('dependencies',
                        nargs='*',
                        help='Android library dependencies')

    # need to move all this catkin stuff to android_init_repo
#    parser.add_argument('-l', '--license',
#                        action='append',
#                        default=["Apache 2.0"],
#                        help='Name for License, (e.g. BSD, MIT, GPLv3...)[BSD]')
#    parser.add_argument('-a', '--author',
#                        action='append',
#                        default=[utils.author_name()],
#                        help='A single author, may be used multiple times')
#    parser.add_argument('-m', '--maintainer',
#                        action='append',
#                        help='A single maintainer, may be used multiple times')
    parser.add_argument('-V', '--pkg_version',
                        action='store',
                        default="0.1.0",
                        help='Initial Package version [0.1.0]')
    parser.add_argument('-D', '--description',
                        action='store',
                        help='Description')
    parser.add_argument('-s', '--sdk-version',
                        action='store',
                        default='17',
                        help='Android sdk version [17]')
    parser.add_argument('-p', '--android-package-name',
                        action='store',
                        default='com.github.rosjava.android.pkg_name',
                        help='Android package name (e.g. com.github.rosjava.android.pkg_name)')
    args = parser.parse_args(argv)
    if args.android_package_name == "com.github.rosjava.android.pkg_name":
        args.android_package_name = "com.github.rosjava.android.%s" % args.name[0].lower()
    if "rosjava_tools" not in args.dependencies:
        args.dependencies.append('rosjava_tools')
    return args


def create_android_project(package_name, sdk_version, java_package_name, is_library):
    path = os.path.join(os.getcwd(), package_name.lower())
    console.pretty_println("\nCreating android project ", console.bold)
    console.pretty_print("  Name      : ", console.cyan)
    console.pretty_println("%s" % package_name, console.yellow)
    console.pretty_print("  Sdk Ver   : ", console.cyan)
    console.pretty_println("%s" % sdk_version, console.yellow)
    console.pretty_print("  Java Name : ", console.cyan)
    console.pretty_println("%s" % java_package_name, console.yellow)
    if is_library:
        console.pretty_print("  Library   : ", console.cyan)
        console.pretty_println("yes\n", console.yellow)
        cmd = ['android', 'create', 'lib-project', '-n', package_name, '-p', path, '-k', java_package_name, '-t', 'android-' + sdk_version, ]
    else:
        activity_name = utils.camel_case(package_name)
        console.pretty_print("  Activity  : ", console.cyan)
        console.pretty_println("%s\n" % activity_name, console.yellow)
        cmd = ['android', 'create', 'project', '-n', package_name, '-p', path, '-k', java_package_name, '-t', 'android-' + sdk_version, '-a', activity_name]
    try:
        subprocess.check_call(cmd)
    except subprocess.CalledProcessError:
        raise subprocess.CalledProcessError("failed to create android project.")
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


def create_catkin_package_files(args, is_library, sdk_version):
    '''
      This is almost a direct copy from catkin_create_pkg.
    '''
    plugin_name = "android-library" if is_library else "android"
    try:
        package_name = args.name[0].lower()
        # Also should move to init repo instead of here.
#        parent_path = os.getcwd()
#        target_path = utils.validate_path(os.path.join(parent_path, package_name))
#        build_depends = []
#        if 'rosjava_tools' not in args.dependencies:
#            build_depends.append('rosjava_tools')
#        for depend_name in args.dependencies:
#            build_depends.append(catkin_pkg.package.Dependency(depend_name))
#        package_template = PackageTemplate._create_package_template(
#            package_name=package_name,
#            description=args.description,
#            licenses=args.license or [],
#            maintainer_names=args.maintainer,
#            author_names=args.author,
#            version=args.pkg_version,
#            catkin_deps=[],
#            system_deps=[],
#            boost_comps=None)
#        package_template.exports = []
#        package_template.build_depends = build_depends
#        package_xml = create_package_xml(package_template=package_template, rosdistro='groovy')
        package_path = os.path.abspath(os.path.join(os.getcwd(), package_name))
        console.pretty_println("\nCreating gradle files", console.bold)
#        try:
#            filename = os.path.join(package_path, 'package.xml')
#            f = open(filename, 'w')
#            f.write(package_xml)
#            console.pretty_print('  File: ', console.cyan)
#            console.pretty_println('package.xml', console.yellow)
#        finally:
#            f.close()
        # Other files
        for template_name in ['build.gradle']:  # 'CMakeLists.txt']:
            filename = os.path.join(package_path, template_name)
            template = read_template_file(template_name)
            contents = instantiate_template(template, package_name, args.author[0], plugin_name, sdk_version)
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


def create_android_package(is_library=False):
    args = parse_arguments()
    create_android_project(args.name[0], args.sdk_version, args.android_package_name, is_library)
    create_catkin_package_files(args, is_library, args.sdk_version)
    add_to_root_gradle_settings(args.name[0])

##############################################################################
# Borrowed from catkin_pkg.package_templates
##############################################################################

from catkin_pkg.package_templates import  _create_depend_tag, \
                PACKAGE_MANIFEST_FILENAME, CatkinTemplate


def read_template_file(filename):
    template_dir = os.path.join(os.path.dirname(__file__), 'templates', 'android_package')
    template = os.path.join(template_dir, '%s.in' % filename)
    if not os.path.isfile(template):
        raise IOError(
            "Could not read template [%s]" % template
        )
    with open(template, 'r') as fhand:
        template_contents = fhand.read()
    return template_contents


def create_package_xml(package_template, rosdistro):
    """
    :param package_template: contains the required information
    :returns: file contents as string
    """
    package_xml_template = read_template_file(PACKAGE_MANIFEST_FILENAME)
    ctemp = CatkinTemplate(package_xml_template)
    temp_dict = {}
    for key in package_template.__slots__:
        temp_dict[key] = getattr(package_template, key)

    if package_template.version_abi:
        temp_dict['version_abi'] = ' abi="%s"' % package_template.version_abi
    else:
        temp_dict['version_abi'] = ''

    if not package_template.description:
        temp_dict['description'] = 'The %s package ...' % package_template.name

    licenses = []
    for plicense in package_template.licenses:
        licenses.append('  <license>%s</license>\n' % plicense)
    temp_dict['licenses'] = ''.join(licenses)

    def get_person_tag(tagname, person):
        email_string = (
            "" if person.email is None else 'email="%s"' % person.email
        )
        return '  <%s %s>%s</%s>\n' % (tagname, email_string,
                                       person.name, tagname)

    maintainers = []
    for maintainer in package_template.maintainers:
        maintainers.append(get_person_tag('maintainer', maintainer))
    temp_dict['maintainers'] = ''.join(maintainers)

    urls = []
    for url in package_template.urls:
        type_string = ("" if url.type is None
                       else 'type="%s"' % url.type)
        urls.append('    <url %s >%s</url>\n' % (type_string, url.url))
    temp_dict['urls'] = ''.join(urls)

    authors = []
    for author in package_template.authors:
        authors.append(get_person_tag('author', author))
    temp_dict['authors'] = ''.join(authors)

    dependencies = []
    dep_map = {
        'build_depend': package_template.build_depends,
        'buildtool_depend': package_template.buildtool_depends,
        'run_depend': package_template.run_depends,
        'test_depend': package_template.test_depends,
        'conflict': package_template.conflicts,
        'replace': package_template.replaces
    }
    for dep_type in ['buildtool_depend', 'build_depend', 'run_depend',
                     'test_depend', 'conflict', 'replace']:
        for dep in sorted(dep_map[dep_type], key=lambda x: x.name):
            if 'depend' in dep_type:
                dep_tag = _create_depend_tag(
                    dep_type,
                    dep.name,
                    dep.version_eq,
                    dep.version_lt,
                    dep.version_lte,
                    dep.version_gt,
                    dep.version_gte
                    )
                dependencies.append(dep_tag)
            else:
                dependencies.append(_create_depend_tag(dep_type,
                                                       dep.name))
    temp_dict['dependencies'] = ''.join(dependencies)

    exports = []
    if package_template.exports is not None:
        for export in package_template.exports:
            if export.content is not None:
                print('WARNING: Create package does not know how to '
                      'serialize exports with content: '
                      '%s, %s, ' % (export.tagname, export.attributes) +
                      '%s' % (export.content),
                      file=sys.stderr)
            else:
                attribs = [' %s="%s"' % (k, v) for (k, v) in export.attributes.items()]
                line = '    <%s%s/>\n' % (export.tagname, ''.join(attribs))
                exports.append(line)
    temp_dict['exports'] = ''.join(exports)

    temp_dict['components'] = package_template.catkin_deps

    return ctemp.substitute(temp_dict)