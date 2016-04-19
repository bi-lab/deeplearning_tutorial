#docker build --rm -t imcomking/ttskc -f Dockerfile_ttskc .

#docker run -it --device /dev/nvidiactl --device /dev/nvidia-uvm --device /dev/nvidia0 -p 22 -p 6006 -p 8888 imcomking/ttskc

#if you want to solve the bug "libdc1394 error: Failed to initialize libdc1394"  
#ln /dev/null /dev/raw1394

##################################

# Start with cuda7.5 base image
# NVIDIA-SMI 352.39     Driver Version: 352.39 
FROM kaixhin/cuda:latest
MAINTAINER Dong-Hyun Kwak <imcomking@gmail.com>

# Install [cudnn 7.0 (v4)]
RUN wget --quiet https://www.dropbox.com/s/dcux1l862p4ml4m/cudnn-7.0-linux-x64-v4.0-rc.tar?dl=0 -O cudnn-7.0-linux-x64-v4.0-rc.tar
RUN tar -xvf cudnn-7.0-linux-x64-v4.0-rc.tar && \
    rm cudnn-7.0-linux-x64-v4.0-rc.tar

RUN ls /cuda/include/cudnn.h
RUN cp /cuda/include/cudnn.h /usr/local/cuda/include/
RUN cp /cuda/lib64/libcudnn.so* /usr/local/cuda/lib64/



# install [caffe]
RUN apt-get update && apt-get install -y --no-install-recommends \
        build-essential \
        cmake \
        git \
        wget \
        libatlas-base-dev \
        libboost-all-dev \
        libgflags-dev \
        libgoogle-glog-dev \
        libhdf5-serial-dev \
        libleveldb-dev \
        liblmdb-dev \
        libopencv-dev \
        libprotobuf-dev \
        libsnappy-dev \
        protobuf-compiler \
        python-dev \
        python-numpy \
        python-pip \
        python-scipy && \
    rm -rf /var/lib/apt/lists/*

ENV CAFFE_ROOT=/opt/caffe
WORKDIR $CAFFE_ROOT

# FIXME: clone a specific git tag and use ARG instead of ENV once DockerHub supports this.
ENV CLONE_TAG=master

RUN git clone -b ${CLONE_TAG} --depth 1 https://github.com/BVLC/caffe.git . && \
    for req in $(cat python/requirements.txt) pydot; do pip install $req; done && \
    mkdir build && cd build && \
    cmake -DUSE_CUDNN=1 .. && \
    make -j"$(nproc)"

ENV PYCAFFE_ROOT $CAFFE_ROOT/python
ENV PYTHONPATH $PYCAFFE_ROOT:$PYTHONPATH
ENV PATH $CAFFE_ROOT/build/tools:$PYCAFFE_ROOT:$PATH
RUN echo "$CAFFE_ROOT/build/lib" >> /etc/ld.so.conf.d/caffe.conf && ldconfig

        
        
        
        
        
        
        
# install [tensorflow]
RUN apt-get update && apt-get install -y \
        # Tensorflow. this is come from the official tensorflow docker file
        build-essential \
        curl \
        git \
        libfreetype6-dev \
        libpng12-dev \
        libzmq3-dev \
        pkg-config \
        python-dev \
        python-numpy \
        python-pip \
        software-properties-common \
        swig \
        zip \
        zlib1g-dev \
        
        # for etc
        python-scipy \
        python-nose \
        python-setuptools \
        python-h5py \ 
        python-matplotlib \
        python-yaml \
        libopenblas-dev \
        screen \ 
        vim \ 
        unzip \
        libatlas-dev \
        libhdf5-dev \
        libatlas3gf-base \
        openssh-server \
        mcrypt \ 
        graphviz \
        && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*
        
        
        
# Install recent pip # this must be done before tensorflow
RUN curl -fSsL -O https://bootstrap.pypa.io/get-pip.py && \
    python get-pip.py && \
    rm get-pip.py
            

# Install Tensorflow
    # Set up Bazel.

# We need to add a custom PPA to pick up JDK8, since trusty doesn't
# have an openjdk8 backport.  openjdk-r is maintained by a reliable contributor:
# Matthias Klose (https://launchpad.net/~doko).  It will do until
# we either update the base image beyond 14.04 or openjdk-8 is
# finally backported to trusty; see e.g.
#   https://bugs.launchpad.net/trusty-backports/+bug/1368094
RUN add-apt-repository -y ppa:openjdk-r/ppa && \
    apt-get update && \
    apt-get install -y openjdk-8-jdk openjdk-8-jre-headless && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Running bazel inside a `docker build` command causes trouble, cf:
#   https://github.com/bazelbuild/bazel/issues/134
# The easiest solution is to set up a bazelrc file forcing --batch.
RUN echo "startup --batch" >>/root/.bazelrc
# Similarly, we need to workaround sandboxing issues:
#   https://github.com/bazelbuild/bazel/issues/418
RUN echo "build --spawn_strategy=standalone --genrule_strategy=standalone" \
    >>/root/.bazelrc
ENV BAZELRC /root/.bazelrc
# Install the most recent bazel release.
ENV BAZEL_VERSION 0.2.1
WORKDIR /
RUN mkdir /bazel && \
    cd /bazel && \
    curl -fSsL -O https://github.com/bazelbuild/bazel/releases/download/$BAZEL_VERSION/bazel-$BAZEL_VERSION-installer-linux-x86_64.sh && \
    curl -fSsL -o /bazel/LICENSE.txt https://raw.githubusercontent.com/bazelbuild/bazel/master/LICENSE.txt && \
    chmod +x bazel-*.sh && \
    ./bazel-$BAZEL_VERSION-installer-linux-x86_64.sh && \
    cd / && \
    rm -f /bazel/bazel-$BAZEL_VERSION-installer-linux-x86_64.sh
    
    
# Download and build TensorFlow.

RUN git clone --recursive https://github.com/tensorflow/tensorflow.git && \
    cd tensorflow && \
    git checkout r0.7
WORKDIR /tensorflow

# Configure the build for our CUDA configuration.
ENV CUDA_TOOLKIT_PATH /usr/local/cuda
ENV CUDNN_INSTALL_PATH /usr/local/cuda
ENV TF_NEED_CUDA 1


# change the setting of protobuf
RUN sed -i "s/kDefaultTotalBytesLimit = 64/kDefaultTotalBytesLimit = 1024/g" google/protobuf/src/google/protobuf/io/coded_stream.h
RUN sed -i "s/kDefaultTotalBytesWarningThreshold = 32/kDefaultTotalBytesWarningThreshold = 1024/g" google/protobuf/src/google/protobuf/io/coded_stream.h


RUN ./configure && \
    bazel build -c opt --config=cuda tensorflow/tools/pip_package:build_pip_package && \
    bazel-bin/tensorflow/tools/pip_package/build_pip_package /tmp/pip && \
    pip install --upgrade /tmp/pip/tensorflow-*.whl
    
# Set up CUDA variables
ENV CUDA_PATH /usr/local/cuda


        
        
# SSH settings  
#RUN apt-get install -y openssh-server mcrypt && \
#    mkdir /var/run/sshd && chmod 0755 /var/run/sshd

RUN mkdir /var/run/sshd && chmod 0755 /var/run/sshd

#ADD https://raw.githubusercontent.com/GeographicaGS/Docker-SFTP/master/sshd_config /etc/ssh/sshd_config
#ADD https://raw.githubusercontent.com/GeographicaGS/Docker-SFTP/master/start.sh /usr/local/bin/start.sh

#my custom files
#ADD https://www.dropbox.com/s/ufu6ckktl4q2vnj/sshd_config?dl=0 /etc/ssh/sshd_config
RUN wget --quiet https://www.dropbox.com/s/ufu6ckktl4q2vnj/sshd_config?dl=0 -O /etc/ssh/sshd_config
#ADD https://www.dropbox.com/s/u94mdss02amvjsz/start.sh?dl=0 /usr/local/bin/start.sh

#VOLUME ["/data"]

#ENTRYPOINT ["/bin/bash"]
#ENTRYPOINT ["/bin/bash", "/usr/local/bin/start.sh"]





# pip install
#RUN pip install --upgrade pip
#RUN pip --no-cache-dir install matplotlib
RUN pip install --upgrade Request

#pydot is not supported under python 3 and pydot2 doesn't work properly. pydotplus works nicely (pip install pydotplus)
RUN pip install pydotplus

# Install [Ipython 3.2.1]
RUN pip install "ipython[notebook]==3.2.1"

# IPython nbserver
RUN ipython profile create nbserver
#RUN cd /root && wget --quiet https://www.dropbox.com/s/7z43hnuza0eb8ba/setup_nbserver_v2.py?dl=0 -O setup_nbserver.py
    
    
    

# Install [Theano]
ENV CUDA_ROOT /usr/local/cuda/bin
RUN pip install --upgrade --no-deps git+git://github.com/Theano/Theano.git
RUN printf "[global]\ndevice=gpu0\nfloatX=float32\ncuda.root=/usr/local/cuda/bin\n[nvcc]\nfastmath=True" > /root/.theanorc

# Gitclone Deeplearning tutorial(theano)
RUN cd /root && git clone git://github.com/lisa-lab/DeepLearningTutorials.git


# Install [Keras]
    
# Upgrade six
RUN pip install --upgrade six

# Clone Keras repo and move into it
RUN cd /root && git clone https://github.com/fchollet/keras.git && cd keras && \
  python setup.py install


# Install [bleeding-edge Lasagne] # this is from Kaixhin's docker file
RUN pip install --upgrade https://github.com/Lasagne/Lasagne/archive/master.zip

# Install [mpld3]
RUN pip install mpld3


# Install [Scikit-learn]
RUN update-alternatives --set libblas.so.3 \
      /usr/lib/atlas-base/atlas/libblas.so.3; \
    update-alternatives --set liblapack.so.3 \
      /usr/lib/atlas-base/atlas/liblapack.so.3

RUN pip install -U scikit-learn




# Install [bleeding-edge JSAnimation]
WORKDIR $HOME
RUN git clone https://github.com/jakevdp/JSAnimation.git
RUN python JSAnimation/setup.py install
ENV PYTHONPATH $PYTHONPATH:$HOME/JSAnimation/:


#RUN apt-get clean && \
    #rm -rf /var/lib/apt/lists/*


# screen setting
RUN printf "\nexport PATH=/usr/local/cuda/bin:$PATH\nexport LD_LIBRARY_PATH=/usr/local/cuda/lib64:$LD_LIBRARY_PATH\n" >> /root/.bashrc
RUN printf "\nshell -/bin/bash\n" >> /root/.screenrc




# TensorBoard
#EXPOSE 6006

# IPython
#EXPOSE 8888
    
# sftp
#EXPOSE 22


#port open for variable purpose. to use these, you should run with '-P' option which opens all exposed port randomly

#EXPOSE 32000 32001 32002 32003 32004
#32005 32006 32007 32008 32009 32010 32011 32012

WORKDIR /root
RUN ["/bin/bash"]

