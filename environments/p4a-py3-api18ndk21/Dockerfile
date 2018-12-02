
FROM ubuntu

ENV SDK_TOOLS="sdk-tools-linux-4333796.zip"
ENV NDK_DL="https://dl.google.com/android/repository/android-ndk-r17c-linux-x86_64.zip"

# Basic image upgrade:
RUN apt update --fix-missing && apt upgrade -y

# Install base packages
RUN apt update && apt install -y zip python3 python-pip cython3 python cython python3-virtualenv python-virtualenv python3-pip curl wget lbzip2 bsdtar && dpkg --add-architecture i386 && apt update && apt install -y build-essential libstdc++6:i386 zlib1g-dev zlib1g:i386 openjdk-8-jdk libncurses5:i386 && apt install -y libtool automake autoconf unzip pkg-config git ant gradle rsync

# Install Android SDK:
RUN mkdir /sdk-install/
RUN cd /sdk-install && wget https://dl.google.com/android/repository/${SDK_TOOLS}
RUN cd /sdk-install && unzip ./sdk-tools-*.zip && chmod +x ./tools//bin/sdkmanager
RUN yes | /sdk-install/tools/bin/sdkmanager --licenses
RUN /sdk-install/tools/bin/sdkmanager --update
RUN /sdk-install/tools/bin/sdkmanager "platform-tools" "platforms;android-28" "build-tools;28.0.3"

# Obtain Android NDK:
RUN mkdir -p /ndk/ && cd /ndk/ && wget ${NDK_DL} && unzip -q android-ndk*.zip

# Install p4a:
RUN {P4A_INSTALL_CMD}

# Final command line preparation:
RUN echo '#!/usr/bin/python3\n\
import json\n\
print("ANDROIDAPI=28" +\n\
    " ANDROIDNDKVER=r17c" +\n\
    " NDKAPI=21" +\n\
    " GRADLE_OPTS=\"-Xms1724m -Xmx5048m -Dorg.gradle.jvmargs='"'"'-Xms1724m -Xmx5048m'"'"'\""+\n\
    " JAVA_OPTS=\"-Xms1724m -Xmx5048m\"" +\n\
    " ANDROIDSDK=/sdk-install/ ANDROIDNDK=/ndk/" +\n\
    " bash")' > /cmdline.py

CMD ["bash", "-c", "bash -c \"`python3 /cmdline.py`\""]



