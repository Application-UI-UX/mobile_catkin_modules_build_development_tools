execute_process(COMMAND "/home/ronaldsonbellande-hplaptop/Desktop/User_Interface_Experience/rosmobile_build_tools/catkin_generated/python_distutils_install.sh" RESULT_VARIABLE res)

if(NOT res EQUAL 0)
  message(FATAL_ERROR "execute_process(/home/ronaldsonbellande-hplaptop/Desktop/User_Interface_Experience/rosmobile_build_tools/catkin_generated/python_distutils_install.sh) returned error code ")
endif()
