#!/usr/bin/python

###############################################################################
#
#   Reset Minecraft
#
#   Copyright Tinker Academy 2014
###############################################################################

import os
import uuid
import sys
import syslog
import subprocess
import urllib2
import tinkeracademy
from tinkeracademy import read_student_id
from tinkeracademy import copy_files
from tinkeracademy import get_course_paths
from tinkeracademy import log_message
from tinkeracademy import log_error
from tinkeracademy import TinkerAcademyMessage
from tinkeracademy import TinkerAcademyConfirmDialog

def reset_minecraft():
	log_message('reset_minecraft enter')
	try:
		subprocess.call(['rm', '-rf', '/home/tinkeracademystudent/.minecraft'])
		msg = 'Minecraft reset successfully'
		gui = TinkerAcademyMessage(msg)
		gui.show()
	except:
		log_message('reset_minecraft failed!')
		log_error()
	log_message('reset_minecraft exit')

def check_reset_minecraft(msg):
	log_message('check_reset_minecraft enter')
	gui = TinkerAcademyConfirmDialog(msg, reset_minecraft)
	gui.show()

def main():
	import time
	t = time.strftime('%X %x %Z')
	log_message('reset_minecraft.py started at ' + str(t))
	msg = 'Are you sure you want to reset Minecraft?'
	check_reset_minecraft(msg)

if __name__ == "__main__":
	main()