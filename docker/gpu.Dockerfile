ARG ROS_ARCHITECTURE_VERSION=latest

FROM ubuntu:20.04 as base_build
FROM nvidia/cuda:11.2.1-base-ubuntu20.04

ENV DEBIAN_FRONTEND noninteractive
ENV PYTHON_VERSION="3.8"
ENV CUDNN_VERSION=8.1.0.77
ENV TF_TENSORRT_VERSION=7.2.2
ENV CUDA=11.2
ENV LD_LIBRARY_PATH /usr/local/cuda/extras/CUPTI/lib64:$LD_LIBRARY_PATH

ARG ROS_ARCHITECTURE_VERSION_GIT_BRANCH=master
ARG ROS_ARCHITECTURE_VERSION_GIT_COMMIT=HEAD

ARG ANDROID_STUDIO_URL=https://dl.google.com/dl/android/studio/ide-zips/3.5.3.0/android-studio-ide-191.6010548-linux.tar.gz
ARG ANDROID_STUDIO_VERSION=3.5

LABEL maintainer=ronaldsonbellande@gmail.com
LABEL ROS_architecture_github_branchtag=${ROS_ARCHITECTURE_VERSION_GIT_BRANCH}
LABEL ROS_architecture_github_commit=${ROS_ARCHITECTURE_VERSION_GIT_COMMIT}

# Ubuntu setup
RUN apt-get update -y
RUN apt-get upgrade -y

# RUN workspace and sourcing
WORKDIR ./
COPY requirements.txt .
COPY system_requirements.txt .
COPY ros_requirements.txt .
COPY ros_repository_requirements.txt .

# Install dependencies for system
RUN apt-get update && apt-get install -y --no-install-recommends <system_requirements.txt \
  && apt-get upgrade -y \
  && apt-get clean \
  && rm -rf /var/lib/apt/lists/*

RUN apt-get update && apt-get install -y wget 
RUN wget "$ANDROID_STUDIO_URL" -O android-studio.tar.gz
RUN tar xzvf android-studio.tar.gz
RUN rm android-studio.tar.gz

# Install python 3.8 and make primary 
RUN apt-get update && apt-get install -y \
  python3.8 python3.8-dev python3-pip python3.8-venv \
  && update-alternatives --install /usr/bin/python python /usr/bin/python3.8 1

# Pip install update 
RUN pip3 install --upgrade pip

# Install python libraries
RUN pip --no-cache-dir install -r requirements.txt

# Install dependencies for ros system 
RUN apt-get update && apt-get install -y --no-install-recommends <ros_requirements.txt \
  && rm -rf /var/lib/apt/lists/*

# Create local catkin workspace
ENV CATKIN_WS=/root/catkin_ws
RUN mkdir -p $CATKIN_WS/src
WORKDIR $CATKIN_WS/src

# Initialize local catkin workspace, install dependencies and build workpsace
RUN echo "source /opt/ros/main/setup.bash" >> ~/.bashrc
RUN source ~/.bashrc

RUN cd $CATKIN_WS \
  && rosdep init \
  && rosdep update \
  && rosdep update --rosdistro main \
  && rosdep fix-permissions \
  && rosdep install -y --from-paths . --ignore-src --rosdistro main

RUN ln -s /studio-data/profile/AndroidStudio$ANDROID_STUDIO_VERSION .AndroidStudio$ANDROID_STUDIO_VERSION
RUN ln -s /studio-data/Android Android
RUN ln -s /studio-data/profile/android .android
RUN ln -s /studio-data/profile/java .java
RUN ln -s /studio-data/profile/gradle .gradle
ENV ANDROID_EMULATOR_USE_SYSTEM_LIBS=1

RUN apt-key adv --fetch-keys https://developer.download.nvidia.com/compute/cuda/repos/ubuntu2004/x86_64/3bf863cc.pub && \
  apt-get update && apt-get install -y --no-install-recommends \
  cuda-nvrtc-${CUDA/./-} \
  libcudnn8=${CUDNN_VERSION}-1+cuda${CUDA} \
  -r cuda_requirements.txt

# We don't install libnvinfer-dev since we don't need to build against TensorRT
RUN apt-key adv --fetch-keys https://developer.download.nvidia.com/compute/machine-learning/repos/ubuntu2004/x86_64/7fa2af80.pub && \
  echo "deb https://developer.download.nvidia.com/compute/machine-learning/repos/ubuntu2004/x86_64 /"  > /etc/apt/sources.list.d/tensorRT.list && \
  apt-get update && \
  apt-get install -y --no-install-recommends libnvinfer7=${TF_TENSORRT_VERSION}-1+cuda11.0 \
  libnvinfer-plugin7=${TF_TENSORRT_VERSION}-1+cuda11.0 \
  && apt-get clean && \
  rm -rf /var/lib/apt/lists/*;

CMD ["bash"]
