#!/usr/bin/python

###############################################################################
#
#   Update Submit
#
#   Copyright Tinker Academy 2015
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
from tinkeracademy import get_other_remote_student_paths
from tinkeracademy import log_message
from tinkeracademy import log_error
from tinkeracademy import TinkerAcademyMessage
from tinkeracademy import TinkerAcademyConfirmDialog

def update_submit():
	log_message('update_submit enter')
	try:
		student_id = read_student_id()
		log_message('update_submit student_id='+str(student_id))
		if student_id:
			log_message('update_submit processing, student_id='+str(student_id))
			other_remote_student_paths = get_other_remote_student_paths(student_id)
			remote_student_path = get_remote_student_path(student_id)
			subprocess.call(['dropbox', 'exclude', 'remove', remote_student_path])
			for other_remote_student_path in other_remote_student_paths:
				subprocess.call(['dropbox', 'exclude', 'add', other_remote_student_path])
		else:
			log_message('update_submit skipping, invalid student_id='+str(student_id))
	except:
		log_message('update_submit failed!')
		log_error()
	log_message('update_submit exit')

def main():
	update_submit()

if __name__ == "__main__":
	main()