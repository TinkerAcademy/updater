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

def reset_submit():
	log_message('reset_submit enter')
	try:
		student_id = read_student_id()
		remote_student_path = get_remote_student_path(student_id)
		subprocess.call(['rm', '-rf', remote_student_path])
		msg = 'Run Course Submit Again after a few minutes!'
		gui = TinkerAcademyMessage(msg)
		gui.show()
	except:
		log_message('reset_submit failed!')
		log_error()
	log_message('reset_submit exit')

def confirm_files_saved_and_closed():
	log_message('confirm_files_saved_and_closed enter')
	msg = 'Have you saved all files and closed all applications?'
	gui = TinkerAcademyConfirmDialog(msg, reset_submit)
	gui.show()

def check_reset_submit(msg):
	log_message('check_reset_submit enter')
	gui = TinkerAcademyConfirmDialog(msg, confirm_files_saved_and_closed)
	gui.show()

def main():
	import time
	t = time.strftime('%X %x %Z')
	log_message('reset_submit.py started at ' + str(t))
	msg = 'Are you sure you want to reset Course Submit?'
	check_reset_submit(msg)

if __name__ == "__main__":
	main()