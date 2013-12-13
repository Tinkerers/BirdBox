#!/bin/bash

# install some stuff
sudo apt-get -y install vim wicd-curses python-pip

# mount frequently-written parts of the FS as ramdisk
cat /etc/fstab > /tmp/fstab
cat >>/tmp/fstab <<END
tmpfs           /tmp            tmpfs   defaults,noatime,mode=1777 0       0
tmpfs           /var/log        tmpfs   defaults,noatime,mode=0755 0       0
tmpfs           /var/lock       tmpfs   defaults,noatime,mode=0755 0       0
END
sudo mv -f /tmp/fstab /etc/fstab

# install BirdBox python requirements
sudo pip install -r requirements.txt
cp settings.py local_settings.py
echo "This is a test message." >> messages.txt

echo "alias go='cd ~/BirdBox && sudo python main.py; cd -'" >> ~/.bashrc
