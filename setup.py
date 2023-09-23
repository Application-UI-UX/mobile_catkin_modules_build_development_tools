#!/usr/bin/env python

from setuptools import setup, find_packages

# Read the contents of README.md for long description
with open('README.md', 'r', encoding='utf-8') as f:
    long_description = f.read()

setup(
    name="mobile_catkin_modules_build_development_tools",
    version="0.4.4",  # Updated version
    description="ROS Mobile Catkin Modules Build Development Tools",
    author="Ronaldson Bellande",
    author_email="ronaldsonbellande@gmail.com",
    long_description=long_description,  # Use the README.md contents as long description
    long_description_content_type="text/markdown",  # Specify the content type as Markdown
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    scripts=[
        'scripts/catkin_create_android_pkg',
        'scripts/catkin_create_android_project',
        'scripts/catkin_create_android_library_project',
        'scripts/catkin_create_rosmobile_pkg',
        'scripts/catkin_create_rosmobile_project',
        'scripts/catkin_create_rosmobile_library_project',
    ],
    package_data = {'mobile_catkin_modules_build_development_tools': [
        'templates/android_package/*',
        'templates/android_project/*',
        'templates/rosmobile_library_project/*',
        'templates/rosmobile_package/*',
        'templates/rosmobile_project/*',
        'templates/init_repo/*',
    ]},
    include_package_data=True,
    install_requires=[
        # List your dependencies here
    ],
    classifiers=[
        "License :: OSI Approved :: Apache Software License",  # Update the classifier here
        "Programming Language :: Python",
    ],
    keywords=["package", "setuptools"],
    python_requires=">=3.0",
    extras_require={
        "dev": ["pytest", "pytest-cov[all]", "mypy", "black"],
    },
    project_urls={
        "Home": "https://github.com/application-ui-ux/mobile_catkin_modules_build_development_tools",
        "Homepage": "https://github.com/application-ui-ux/mobile_catkin_modules_build_development_tools",
        "documentation": "https://github.com/application-ui-ux/mobile_catkin_modules_build_development_tools",
        "repository": "https://github.com/application-ui-ux/mobile_catkin_modules_build_development_tools",
    },
)
