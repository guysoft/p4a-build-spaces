
FROM ubuntu:20.04

ENV SDK_TOOLS="sdk-tools-linux-4333796.zip"
ENV NDK_DL="https://dl.google.com/android/repository/android-ndk-r17c-linux-x86_64.zip"
ENV NDKVER=r17c
ENV NDKDIR=/ndk/
ENV NDKAPI=21
ENV ANDROIDAPI=28
ENV PIP=pip3

# Basic image upgrade:
RUN apt update --fix-missing && apt upgrade -y

# Install base packages
# RUN apt update && apt install -y zip python3 python-pip python python3-virtualenv python-virtualenv python3-pip curl wget lbzip2 bsdtar && dpkg --add-architecture i386 && apt update && apt install -y build-essential libstdc++6:i386 zlib1g-dev zlib1g:i386 openjdk-8-jdk libncurses5:i386 && apt install -y libtool automake autoconf unzip pkg-config git ant gradle rsync

RUN set -x \
    && apt-get update && apt-get install -y \
        build-essential \
        curl \
        git \
        wget \
        p7zip-full \
        python3 \
        sudo \
        git \
        zip \
        unzip \
        openjdk-17-jdk \
        autoconf \
        libtool \
        pkg-config \
        zlib1g-dev \
        libncurses5-dev \
        libncursesw5-dev \
        libtinfo5 \
        cmake \
        libffi-dev \
        libssl-dev \
  && rm -rf /var/lib/apt/lists/* \
  && apt -qyy clean
    
#========================================
# Add normal user with passwordless sudo
#========================================
# Layer size: tiny: 0.3 MB
RUN useradd ubuntu \
         --shell /bin/bash  \
         --create-home \
  && usermod -a -G sudo ubuntu \
  && gpasswd -a ubuntu video \
  && echo 'ubuntu:secret' | chpasswd \
&& echo 'ALL ALL = (ALL) NOPASSWD: ALL' >> /etc/sudoers

RUN wget --no-check-certificate https://bootstrap.pypa.io/get-pip.py -O - | python3
RUN pip3 install --upgrade Cython==0.29.33
RUN pip3 install --upgrade buildozer



# Install Android SDK:
RUN mkdir /sdk-install/
RUN cd /sdk-install && wget https://dl.google.com/android/repository/${SDK_TOOLS}
RUN cd /sdk-install && unzip ./sdk-tools-*.zip && chmod +x ./tools//bin/sdkmanager
RUN yes | /sdk-install/tools/bin/sdkmanager --licenses
RUN /sdk-install/tools/bin/sdkmanager --update
RUN /sdk-install/tools/bin/sdkmanager "platform-tools" "platforms;android-28" "build-tools;28.0.3"

# Obtain Android NDK:
RUN mkdir -p /tmp/ndk/ && cd /tmp/ndk/ && wget ${NDK_DL} && unzip -q android-ndk*.zip && mv android-*/ /ndk/

# Install shared packages:
{INSTALL_SHARED_PACKAGES}

# Install p4a:
RUN {P4A_INSTALL_CMD}

{TEST_APP_INSTRUCTIONS}



