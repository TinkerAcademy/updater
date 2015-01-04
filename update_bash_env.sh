#!/bin/bash
###############################################################################
## Update Bash Environment 
## 
## Copyright Tinker Academy 2014
###############################################################################

##
## Update Minecraft Client Home
##

cd
EXISTS_MINECRAFT_HOME=`cat /home/tinkeracademystudent/.bash_profile | grep MINECRAFT_CLIENT_HOME`
echo "["$EXISTS_MINECRAFT_HOME"]"
if [ -z "$EXISTS_MINECRAFT_HOME" ]
then
  echo "export MINECRAFT_CLIENT_HOME=/home/tinkeracademystudent/Documents/minecraft/client" >> .bash_profile
else
  echo "\$MINECRAFT_CLIENT_HOME already exists"
fi

##
## Update .profile to invoke .bash_profile
##
cd
EXISTS_BASH_PROFILE=`cat /home/tinkeracademystudent/.profile | grep BASH_PROFILE`
echo "["$EXISTS_BASH_PROFILE"]"
if [ -z "$EXISTS_BASH_PROFILE" ]
then
  echo "export BASH_PROFILE=/home/tinkeracademystudent/.bash_profile" >> .profile
  echo ". \$BASH_PROFILE" >> .profile
else
  echo "\$BASH_PROFILE already exists"
fi
source /home/tinkeracademystudent/.profile
