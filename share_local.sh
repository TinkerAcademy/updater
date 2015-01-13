###############################################################################
## 
## Script to zip and locally share 
##     
## Copyright Tinker Academy 2014
###############################################################################
export UPDATE_DATE=`date +%Y-%m-%d`
export DROPBOX_PATH="/Users/ron/Dropbox"
export COURSEUPDATE_PATH="/Users/ron/Documents/TinkerAcademy/WebRoot"
export COURSEUPDATE_FILENAME=courseupdate$UPDATE_DATE
export IP_ADDRESS=`ifconfig | grep -A 4 en1: | grep inet | grep -v inet6 | cut -d' ' -f2`
export TARGET_FILENAME=CourseUpdate$UPDATE_DATE.zip
export WEBSERVER_PATH="/Users/ron/Documents/mongoose"
export JETTY_HOME="/Users/ron/Documents/jetty"
pushd `pwd`
rm -rf $COURSEUPDATE_PATH/$COURSEUPDATE_FILENAME
cp -rp $DROPBOX_PATH/classes $COURSEUPDATE_PATH/$COURSEUPDATE_FILENAME
cd $COURSEUPDATE_PATH
rm -rf $TARGET_FILENAME
cd $COURSEUPDATE_FILENAME
ln -s scripts/update_course.py "Course Update"
chmod u+x "Course Update"
mkdir -p maintenance
cd maintenance
ln -s ../scripts/update_bash_env.sh "Update Environment"
ln -s ../scripts/restart_dropbox.sh "Restart Dropbox"
ln -s ../scripts/reset_minecraft.py "Reset Minecraft"
chmod u+x "Update Environment"
chmod u+x "Restart Dropbox"
chmod u+x "Reset Minecraft"
cd $COURSEUPDATE_PATH
zip -y -r $TARGET_FILENAME $COURSEUPDATE_FILENAME 
echo $TARGET_FILENAME created
rm -rf $COURSEUPDATE_PATH/$COURSEUPDATE_FILENAME
popd
pushd .
echo "IP_ADDRESS ["$IP_ADDRESS"]"
#cd $WEBSERVER_PATH
#sudo ./mongoose -listening_ports 80 -document_root $COURSEUPDATE_PATH
cd $JETTY_HOME
sudo java -jar start.jar 
popd
