# Raspberry Pi OS installation:
1. Go to https://www.raspberrypi.org/downloads/raspbian/ or https://www.raspberrypi.org/software/
2. Download Raspbian Stretch with desktop and recommended software (as example) or download Imager
3. Unpack it
4. Download Win32 Disk Imager or ODIN https://sourceforge.net/projects/win32diskimager/
5. Upload image of SD-card
6. Put SD-card in device and run

## Further OS basic instructions:
```bash
sudo su
raspi-config
apt-get update
apt-get upgrade
apt-get autoremove
```

## For audio:
1. [Audio configuration](https://www.raspberrypi.org/documentation/configuration/audio-config.md)
2. [Connect bluetooth devices](https://youness.net/raspberry-pi/bluetooth-headset-raspberry-pi)

## Enabling remote connecting to desktop:
```bash
sudo apt-get install ssh
sudo apt-get install xrdp
# reboot

sudo /etc/init.d/ssh start
sudo /etc/init.d/xrdp start

# Start ssh on startup
sudo systemctl enable ssh

sudo raspi-config
##  5 Interfacing Options
## P2 SSH
## Yes
## P1 Camera for Camera socket on device
```

## Auto wlan0:
```bash
sudo nano /etc/network/interfaces


```

## Get device address:
1. ifconfig in command line
2. Copy ip addr that is address for device
3. Paste on your machine (SSH, Remote Microsoft Windows Connection with inrerface)

## [Installing TeamViewer](https://community.teamviewer.com/t5/TeamViewer-IoT-Support/Teamviewer-12-for-Raspberry-Pi/td-p/27312):
```bash
wget http://download.teamviewer.com/download/linux/version_11x/teamviewer-host_armhf.deb

sudo apt update

sudo apt install ./teamviewer-host_armhf.deb
```

## Git commands:
```bash
cd Desktop
mkdir mygithub
sudo apt-get install git
git clone https://github.com/nikitawow1337/Presence-detection
cd Presence-detection
git config user.name test123
git config user.email test123@gmail.com
git config credential.helper store
```

## Install OpenCV:
Better to follow [the guide](https://www.learnopencv.com/install-opencv3-on-ubuntu/)



```bash
# ~21 3.5 12.3 170 48 1.4 1 2 4 MB
sudo apt-get install libavcodec-dev libavformat-dev libswscale-dev libdc1394-22-dev
sudo apt-get install libxine2-dev libv4l-dev
sudo apt-get install libgstreamer0.10-dev libgstreamer-plugins-base0.10-dev
sudo apt-get install qt5-default libgtk2.0-dev libtbb-dev
sudo apt-get install libatlas-base-dev
sudo apt-get install libfaac-dev libmp3lame-dev libtheora-dev
sudo apt-get install libvorbis-dev libxvidcore-dev
sudo apt-get install libopencore-amrnb-dev libopencore-amrwb-dev
sudo apt-get install x264 v4l-utils
```

# Install python libraries
```bash
sudo apt-get install python-dev python-pip python3-dev python3-pip
sudo -H pip2 install -U pip numpy
sudo -H pip3 install -U pip numpy
```

Install OpenCV:
```bash
# installing most libraries that are not in system; some of libraries can have different name
sudo apt-get -y install build-essential cmake cmake-qt-gui pkg-config libpng12-0 libpng12-dev libpnglite-dev zlib1g-dbg zlib1g zlib1g-dev pngtools libtiff4 libtiffxx0c2 libtiff-tools
# downloading OpenCV from sourceforge, latest version (30.3.2019)
wget https://sourceforge.net/projects/opencvlibrary/files/4.0.1/OpenCV\ 4.0.1.zip
# unpacking archive
unzip -d OpenCV-4.0.1 OpenCV\ 4.0.1.zip
# create build directory
cd OpenCV-4.0.1
mkdir build && cd build
# building files with python support and examples
cmake -D CMAKE_BUILD_TYPE=RELEASE \
      -D CMAKE_INSTALL_PREFIX=/usr/local \
      -D INSTALL_C_EXAMPLES=ON \
      -D INSTALL_PYTHON_EXAMPLES=ON \
      -D WITH_TBB=ON \
      -D WITH_V4L=ON \
      -D WITH_QT=ON \
      -D WITH_OPENGL=ON \
      -D BUILD_EXAMPLES=ON ..
# check how many available cores you have
nproc
# make can last 9-10 hours depends on what Raspberry is used, better time with compiling it on 2 or 4 cores
make -j4
# installing files in directory
make install
sudo sh -c 'echo "/usr/local/lib" >> /etc/ld.so.conf.d/opencv.conf'
sudo ldconfig
# try to find files in your local lib directory
find /usr/local/lib/ -type f -name "cv2*.so"
# if nothing was fonud do this command, depends what version of Python is used
cp cv2.so /usr/local/lib
```

## Running examples

First example:
```bash
cd Presence-detection/examples
python example1.py
```

Second example:
```
git clone https://github.com/opencv/opencv
cp opencv/data/haarcascades/haarcascade_frontalface_default.xml Presence-detection/examples/
python example2.py
```

## Install required libraries for face_recognition:
```python
# install it through pip3 install (except face_recognition and vlc that will be described later)
import face_recognition 
import time 
import threading 
from gtts import gTTS 
import vlc 
import random 
import sys 
from imutils import paths 
import pickle 
import cv2 
import os 
import argparse 
import datetime
```

## Install [face_recognition](https://gist.github.com/ageitgey/1ac8dbe8572f3f533df6269dab35df65):
```bash

# seems that it works only on latest Raspbian Jessie Light
sudo raspi-config -> Advanced -> gpu memory split -> 16
# enable a larger swap file to size
sudo nano /etc/dphys-swapfile
change variable: CONF_SWAPSIZE=1024
# restart swap to make it enabled
sudo /etc/init.d/dphys-swapfile restart
# install dlib
mkdir dlib
git clone -b 'v19.6' --single-branch https://github.com/davisking/dlib.git dlib/
cd ./dlib
sudo python3 setup.py install --compiler-flags "-mfpu=neon"
# install face_recognition
sudo pip3 install face_recognition
# change swapfile and gpu to default settings
```

## Install PulseAudio:
```bash
sudo apt-get remove --purge alsa-base pulseaudio
sudo apt-get install alsa-base pulseaudio
sudo apt-get -f install && sudo apt-get -y autoremove && sudo apt-get autoclean && sudo apt-get clean
sudo reboot
pulseaudio --start
```

## Install vlc:
```bash
# install vlc in system
sudo apt-get install vlc
# install python-vlc in python enviroment, do not install vlc (pip install vlc)!
sudo pip3 install python-vlc
# try it in enviroment
python3
import vlc
vlc_instance = vlc.Instance()
player = vlc_instance.media_player_new()
# must be no errors
```

## Install vlc manually (if previous case doesn't work):
```bash
# helpful links:
https://thepi.io/how-to-compile-vlc-media-player-with-hardware-acceleration-for-the-raspberry-pi/
https://github.com/matthiasbock/Mini-Xplus-Firmware/issues/20
# purge previous versions of vlc
sudo apt-get purge vlc
# get vlc from videolan.org (3.0.6 version is latest, 10 Jan 2019)  
wget http://download.videolan.org/vlc/3.0.6/vlc-3.0.6.tar.xz 
# unpack archive
tar -xJf vlc-3.0.6.tar.xz
sudo apt-get install libxcb-composite0 libxcb-composite0-dev libtwolame-dev liba52-0.7.4-dev libxcb-composite0-dev libxcb-glx0-dev libxcb-dri2-0-dev libxcb-xf86dri0-dev libxcb-xinerama0-dev libxcb-render-util0-dev libxcb-xv0-dev
sudo apt-get install libdca-dev libflac-dev libmpeg2-4-dev libspeexdsp-dev libschroedinger-dev libdirac-dev libfluidsynth-dev libkate-dev liboggkate-dev libxcb-shm0-dev libxcb-composite0-dev libxcb-glx0-dev libxcb-dri2-0-dev libxcb-xf86dri0-dev libxcb-xinerama0-dev libxcb-render-util0-dev libxcb-xv0-devlibxcb-keysyms1-dev libxcb-randr0-dev libgl1-mesa-dev libgl1-mesa-dev libqt4-dev libfribidi-dev libsdl1.2-dev libass-dev librsvg2-dev libcaca-dev libportaudio-dev libsamplerate0-dev libudev-dev libmtp-dev libupnp-dev alsa-lib
sudo apt-get install autopoint gettext liba52-0.7.4-dev libaa1-dev libasound2-dev libass-dev libavahi-client-dev libavc1394-dev libavcodec-dev libavformat-dev libbluray-dev libcaca-dev libcddb2-dev libcdio-dev libchromaprint-dev libdbus-1-dev libdc1394-22-dev libdca-dev libdirectfb-dev libdvbpsi-dev libdvdnav-dev libdvdread-dev libegl1-mesa-dev libfaad-dev libflac-dev libfluidsynth-dev libfreerdp-dev libfreetype6-dev libfribidi-dev libgl1-mesa-dev libgles1-mesa-dev libgles2-mesa-dev libgnutls28-dev libgtk2.0-dev libidn11-dev libiso9660-dev libjack-jackd2-dev libkate-dev liblircclient-dev liblivemedia-dev liblua5.2-dev libmad0-dev libmatroska-dev libmodplug-dev libmpcdec-dev libmpeg2-4-dev libmtp-dev libncursesw5-dev libnotify-dev libogg-dev libomxil-bellagio-dev libopus-dev libpng12-dev libpulse-dev libqt4-dev libraw1394-dev libresid-builder-dev librsvg2-dev libsamplerate0-dev libschroedinger-dev libsdl-image1.2-dev libsdl1.2-dev libshine-dev libshout3-dev libsidplay2-dev libsmbclient-dev libspeex-dev libspeexdsp-dev libssh2-1-dev libswscale-dev libtag1-dev libtheora-dev libtwolame-dev libudev-dev libupnp-dev libv4l-dev libva-dev libvcdinfo-dev libvdpau-dev libvncserver-dev libvorbis-dev libx11-dev libx264-dev libxcb-composite0-dev libxcb-keysyms1-dev libxcb-randr0-dev libxcb-shm0-dev libxcb-xv0-dev libxcb1-dev libxext-dev libxinerama-dev libxml2-dev libxpm-dev libzvbi-dev lua5.2 oss4-dev pkg-config zlib1g-dev libtool build-essential autoconf
# here can be errors with libpng, liblang, better to install dependencies, ignore versions
# go to directory
cd vlc-3.0.6
# run script
./bootstrap
# cmake
CFLAGS="-I/opt/vc/include/ -I/opt/vc/include/interface/vcos/pthreads -I/opt/vc/include/interface/vmcs_host/linux -I/opt/vc/include/interface/mmal -I/opt/vc/include/interface/vchiq_arm -I/opt/vc/include/IL -I/opt/vc/include/GLES2 -mfloat-abi=hard -mcpu=cortex-a7 -mfpu=neon-vfpv4" CXXFLAGS="-I/opt/vc/include/ -I/opt/vc/include/interface/vcos/pthreads -I/opt/vc/include/interface/vmcs_host/linux -I/opt/vc/include/interface/mmal -I/opt/vc/include/interface/vchiq_arm -I/opt/vc/include/IL -mfloat-abi=hard -I/opt/vc/include/GLES2 -mcpu=cortex-a7 -mfpu=neon-vfpv4" LDFLAGS="-L/opt/vc/lib" ./configure --prefix=/usr --enable-omxil --enable-omxil-vout --enable-rpi-omxil --disable-mmal-codec --disable-mmal-vout --enable-gles2 --disable-lua --disable-a52 --disable-alsa
# make
make -j4
# make install
make install
```

## Possible bugs/errors:
 libjasper.so.1: cannot open shared object file: No such file or directory.

 Solution: https://github.com/amymcgovern/pyparrot/issues/34
