#!/bin/bash
###############################################################################
## Reinstall Dropbox
## 
## Copyright Tinker Academy 2014
###############################################################################
export DROPBOX=/home/tinkeracademystudent/.dropbox
export DROPBOXD=/home/tinkeracademystudent/.dropbox-dist/dropboxd
cd
if [ ! -d $DROPBOX ];
then
  echo "\$DROPBOX does not exist. Unable to proceed. Email classes@tinkeracademy.com for help."
else
	if [ ! -f $DROPBOXD ];
	then
	  wget -O - "https://www.dropbox.com/download?plat=lnx.x86" | tar xzf -
	else
	  echo "\$DROPBOXD already exists"
	fi
	$DROPBOXD
fi



