^^^^^^^^^
Changelog
^^^^^^^^^

0.4.4 (2023-09-14)
------------------
* Fix countless bugs in the repository 
* Rerelease dedicated code for maven, ros, and python
* Change name for more discriptions a take down old publish namees
* Make repository compatible with ROS2 and will now be compatible for ROS1 and ROS2
* Upgrade version of all builds and make it more compatible
* Maintainer & Contributors & Aurthor: Ronaldson Bellande

0.4.2 (2023-09-11)
------------------
* Fix countless bugs in the repository and recalibrate
* Release dedicated code for maven, ros, and python 
* Maintainer & Contributors & Aurthor: Ronaldson Bellande

0.4.1 (2022-05-19)
------------------
* Update package.xml, CMakeList.txt for main branch
* Update gradle and wapper to be up-to-date
* Fix Bugs that has to do with the gradle building
* Release version in github for easy access when building project
* Maintainer & Contributors & Aurthor: Ronaldson Bellande

0.3.3 (2019-01-17)
------------------
* Fixed problem to find gradlew when cross-compiling.
* Gradle 2.14.1 --> 4.10.2.
* Fix for genjava ignoring most packages in standalone mode.
* Contributors: Johannes Meyer, Juan Ignacio Ubeira, Julian Cerruti, ivanpauno

0.3.2 (2016-12-29)
------------------
* Changed default Gradle target publishMavenJavaPublicationToMavenRepository -> publish
* Contributors: Julian Cerruti

0.3.1 (2016-12-27)
------------------
* Gradle 2.2.1 -> 2.14.1

0.3.0 (2016-12-14)
------------------
* Updates for Kinetic release.

0.2.4 (2015-06-03)
------------------
* bugfix environment hooks for workspaces with spaces.

0.2.3 (2015-03-01)
------------------
* publically expose the rosmobile environment setup (for genjava).
* Contributors: Daniel Stonier

0.2.2 (2015-02-25)
------------------
* support for finding broken message packages.
* Contributors: Daniel Stonier

0.2.1 (2015-02-25)
------------------
* upgrade catkin create scripts for indigo
* support modules for genjava
* deprecated create msg package scripts
* minor bugfixes and improvements.
* Contributors: Benjamin Chrétien, Daniel Stonier, Martin Pecka

0.2.0 [2013-10-25]
------------------
* official maven style open range dependencies in templates
* gradle 1.7->1.8
* android build tools 18.1.1

0.1.34 (20.4.46-12)
--------------------
* assist rospack to speedup by ignoring the installed maven directories.

0.1.33 [20.4.43-19]
--------------------
* gradle 1.9->1.11

0.1.32 [2014.12-20]
--------------------
* bugfix catkin_make on empty catkin_created gradle projects.

0.1.31 [2014.12-03]
--------------------
* separate app and library catkin_create_rosmobile_xxx_project scripts.
* app rosmobile project integration with catkin_make (i.e. cmake-gradle targets).

0.1.30 [2013-12-26]
-------------------
* rosdistro scraping more intelligent now checks for message_generation dependant packages
* gradle 1.8->1.9 upgrade in templates

0.1.29 [2013-11-08]
-------------------
* fix single artifact message generation when there is dependencies.

0.1.28 [2013-10-30]
-------------------
* seed ROS_MAVEN_REPOSITORY when necessary.

0.1.27 [2013-10-30]
-------------------
* use ROS_MAVEN_REPOSITORY to configure the external repository.

0.1.26 [2013-10-26]
-------------------
* embedded gradle 1.7->1.8
* templates updated for official maven style open ranged dependencies

0.1.25 [2013-10-26]
-------------------
* gradle 1.7->1.8
* android tools 17->18.1.1

0.1.24 [2013-10-04]
-------------------
* bugfix for missing catkin_create_rosmobile_xxx templates.

0.1.17-23 [2013-09-26]
----------------------
* catkin_create_rosmobile_xxx scripts added.

0.1.17-22 [2013-09-23]
----------------------
* Use GRADLE_USER_HOME only when creating binaries.
* Use maven-publish for publishing rosmobile packages
* Catkin-gradle environment variable bugfixes.
* Allow user environment variables to override automatic rosmobile settings.
* Add install rule for environemnt generation script.

0.1.16 [2013-09-17]
-------------------

* Fix rosmobile environment hooks so they work in chained workspaces.
* Bring the gradle user home into the development workspace as well (fix build farm problems).

0.1.15 [2013-09-13]
-------------------
* Fix dependency on rosinstall-generator

0.1.14 [2013-09-13]
-------------------
* Swtich to rosjava_build_tools.

0.1.13 [2013-09-10]
-------------------
* Ros maven repo environment preparation (bash + cmake).

0.1.12 [2013-09-01]
-------------------
* Add catkin dependency.

0.1.11 [2013-09-01]
-------------------
* Redirect maven repos from robotbrain->rosmobile for template scripts.

0.1.10 [2013-08-14]
-------------------
* Fix spanish encoding problems on android_create_repo.

0.1.9 [2013-08-08]
------------------
* Fix install permissions for gradlew script

0.1.8 [2013-07-15]
------------------
* Upgrade android gradle plugin to 0.5.0 (android studio 0.2.0).

0.1.7 [2013-07-04]
------------------
* Bugfix to add missing gradle wrapper jar.

0.1.6 [2013-06-26]
------------------
* Revert maven-publish plugin

0.1.5 [2013-06-10]
------------------
* Bugfix rosmobile install targets

0.1.4 [2013-06-10]
------------------
* Publish to maven local with the maven-publish plugin.

0.1.3 [2013-06-04]
------------------
* Bugfix android create scripts for 1-1 repo-package style.

0.1.2 [2013-06-03]
------------------
* Bugfix missing template files for the creation scripts.

0.1.1 [2013-05-30]
------------------
* Cmake java and android helpers
* Android catkin_create_repo/pkg/library creation scripts.
