mkdir -p /tmp/prerelease_job
cd /tmp/prerelease_job
generate_prerelease_script.py \
  https://raw.githubusercontent.com/ros-infrastructure/ros_buildfarm_config/production/index.yaml \
  noetic default ubuntu focal amd64 \
  --custom-repo \
    mobile_catkin_modules_build_development_tools__custom-1:git:https://github.com/Application-UI-UX/mobile_catkin_modules_build_development_tools:main \
  --level 1 \
  --output-dir ./
