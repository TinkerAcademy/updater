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
from tinkeracademy import get_remote_student_path
from tinkeracademy import log_message
from tinkeracademy import log_error
from tinkeracademy import TinkerAcademyMessage
from tinkeracademy import TinkerAcademyConfirmDialog

def poweroff():
	log_message('poweroff enter')
	try:
		subprocess.call(['echo', '-rf', remote_student_path])
		ps = subprocess.Popen(('echo', 'tinker2015'), stdout=subprocess.PIPE)
		ps2 = subprocess.Popen(('sudo', '-S', 'poweroff'), stdin = ps.stdout, stdout=subprocess.PIPE)
		output = ps2.communicate()[0]
		if output:
			log_message(output)
			print output
		ps.stdout.close()
	except:
		log_message('poweroff failed!')
		log_error()
	log_message('poweroff exit')

def check_poweroff(msg):
	log_message('check_poweroff enter')
	gui = TinkerAcademyConfirmDialog(msg, poweroff)
	gui.show()

def main():
	import time
	t = time.strftime('%X %x %Z')
	log_message('poweroff.py started at ' + str(t))
	msg = 'Are you sure you want to poweroff the machine?'
	check_poweroff(msg)

if __name__ == "__main__":
	main()