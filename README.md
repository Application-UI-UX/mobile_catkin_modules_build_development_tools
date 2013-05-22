# RosJava Tools

Build tools for rosjava and android repositories. Currently only includes tools for the rosjava repositories which are
quite trivial, just a cmake macro. The android repository support has been done, but waiting to see how the android
gradle plugin goes before dropping them back in here.


## RosJava Demo


```
> mkdir -p ~/rosjava/src
> cd ~/rosjava/src
> catkin_init_workspace .
> wstool init .
> wstool set rosjava_tools --git https://github.com/ros-java/rosjava_tools -v hydro-devel
> wstool set rosjava_core --git https://github.com/stonier/rosjava_core -v catkin_tools
> wstool update
> cd ~/rosjava
> catkin_make
```

The only changes made to the `rosjava_core` repo was to add a `package.xml` with a depends on `rosjava_tools` and a
changes to the `CMakeLists.txt` as follows:

```
...
find_package(catkin REQUIRED rosjava_tools)

catkin_rosjava_setup(install)
```

This cmake makro sets up dummy targets in the cmake configuration which call out to gradle in the actual make step. 
It also parses the `package.xml` to add target dependencies from each `build_depends` tag (subsequently letting you
sequence builds across repositories).

It also adds a global and package `gradle-clean` target.

```
> catkin_make
# Clean a single gradle package
> cd ~/rosjava/build/rosjava_core
> make gradle-clean-rosjava_core
# Clean all gradle packages
> cd ~/rosjava/build
> make gradle-clean
```
