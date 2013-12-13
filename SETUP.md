Setup instructions for a new raspi

. Download and install raspbian to a fresh SD card
	install directions: http://elinux.org/RPi_Easy_SD_Card_Setup
. boot pi
. initial config from config utility
	a. advanced options -> update
	b. expand filesystem
	c. change password
	d. Advanced options
		i. change hostname
		ii. memory split to 16M
		iii. enable ssh
. sudo apt-get update && sudo apt-get upgrade
. sudo apt-get install avahi-daemon
. reboot
. log in via ssh
. git clone this repo
