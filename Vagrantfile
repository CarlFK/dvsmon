# -*- mode: ruby -*-
# vi: set ft=ruby :

$script = <<SCRIPT

apt-get --assume-yes update

# use local cache if it exists:
apt-get --assume-yes install squid-deb-proxy-client
apt-get --assume-yes upgrade

# install things to keep me from going crazy
apt-get --assume-yes install git dpkg-dev vim python-software-properties

# apt-add-repository --yes ppa:carlfk
# apt-add-repository --yes "deb http://ftp.us.debian.org/debian wheezy-backports main"
# apt-get --assume-yes update
# apt-get --assume-yes upgrade

# install dev tools
apt-get --assume-yes install git dpkg-dev

# deps for dvs-mon
apt-get --assume-yes install dvswitch dvsource dvsink python-wxgtk2.8

# deps for building dvswitch
# apt-get --assume-yes install cmake libasound2-dev libavcodec-dev libboost-dev libboost-thread-dev libboost-system-dev libgtkmm-2.4-dev libjack-jackd2-dev liblo-dev libraw1394-dev libxv-dev

# deps for gst-plugins-dvswitch
# apt-get --assume-yes install dh-autoreconf libgstreamer-plugins-base0.10-dev gstreamer0.10-ffmpeg
apt-get --assume-yes install dh-autoreconf libgstreamer-plugins-base1.0-dev gstreamer1.0-libav

# deps for dvsource-v4l2-other
apt-get --assume-yes install \
  gstreamer0.10-tools \
  gstreamer0.10-plugins-base \
  gstreamer0.10-plugins-good \
  gstreamer0.10-ffmpeg \
  libgstreamer0.10-0

apt-get --assume-yes install \
  gstreamer1.0-tools \
  gstreamer1.0-plugins-base \
  gstreamer1.0-plugins-good \
  gstreamer1.0-avlib \
  libgstreamer1.0-0


# install things to support autorunning a gui app
# apt-get --assume-yes install ubuntu-desktop
# install less than the whole u-desktop (and apps):
apt-get --assume-yes install xorg lightdm xubuntu-default-settings xfce4-session

# auto log in the vagrant user
printf "autologin-user=${account}\n" >> /etc/lightdm/lightdm.conf

# things to do as the user (vagrant)
cat <<B2 >bootstrap2.sh
#!/bin/bash -x

mkdir bin

# setup .dvswitchrc 
cat <<dvsrc > .dvswitchrc
MIXER_HOST=0.0.0.0
MIXER_PORT=2000
dvsrc

# build dvswitch
# git clone git://git.debian.org/git/dvswitch/dvswitch.git
# cd dvswitch
# dpkg-buildpackage -b
# cd ..
# sudo dpkg -i  ???

# build/install gst-plugins-dvswitch
git clone git://github.com/timvideos/gst-plugins-dvswitch.git
cd gst-plugins-dvswitch
dpkg-buildpackage -b
cd ..
# sudo dpkg --install gstreamer0.10-dvswitch*.deb
sudo dpkg -i gstreamer0.10-dvswitch_0.0.1-1_amd64.deb

# build/install dvsource-v4l2-other
git clone https://github.com/timvideos/dvsource-v4l2-other.git
# there is no setup, so put a link in ~/bin which is in PATH
cd bin
ln -s ~/dvsource-v4l2-other/dvsource-v4l2-other
cd

git clone git://github.com/CarlFK/dvsmon.git

# .config doesn't exist yet (guessing it gets created after the first login)
mkdir -p .config/autostart
cat <<AUTORUN > .config/autostart/dvsmon.desktop
[Desktop Entry]
Type=Application
Exec=/bin/bash -c "cd /home/vagrant/dvsmon && ./stream_test.sh -k 4"
Name=DVswitch-monitor
AUTORUN

# eof: bootstrap2.sh
B2
chown vagrant ./bootstrap2.sh
chmod u+x ./bootstrap2.sh
su vagrant ./bootstrap2.sh

# boot into X, ./stream_test.sh will then run 
service lightdm start

SCRIPT

VAGRANTFILE_API_VERSION = "2"
Vagrant.configure(VAGRANTFILE_API_VERSION) do |config|

  config.vm.box = "precise64"
  config.vm.box_url = "http://files.vagrantup.com/precise64.box"
  config.vm.provision "shell", inline: $script
  config.vm.network "forwarded_port", guest: 2000, host: 2000,
      auto_correct: true

  config.vm.provider :virtualbox do |vb|
     vb.gui = true
     vb.customize ["modifyvm", :id, "--memory", "512"]
     vb.customize ["modifyvm", :id, "--cpus", "1"]
     vb.customize ["modifyvm", :id, "--cpuexecutioncap", "90"]
  end

end

