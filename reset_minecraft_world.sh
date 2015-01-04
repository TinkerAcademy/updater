#!/bin/bash
MINECRAFT_HOME=/home/tinkeracademystudent/Documents/minecraft/server
pushd .
cd $MINECRAFT_HOME/world || exit 1
rm -rf *
popd

pushd .
cd $MINECRAFT_HOME/world_nether || exit 1
rm -rf *
popd

pushd .
cd $MINECRAFT_HOME/world_the_end || exit 1
rm -rf *
popd
