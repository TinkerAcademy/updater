#!/usr/bin/python

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
from tinkeracademy import log_error
from tinkeracademy import log_message
from tinkeracademy import TinkerAcademyMessage

BASE_LOCAL='/home/student/Documents/tinkeracademy/Courses'
BASE_REMOTE='/home/student/.Dropbox/Dropbox/students/'

def copy_local_to_remote():
	log_message('copy_local_to_remote enter')
	ret = -1
	student_id = read_student_id()
	log_message('copy_local_to_remote student_id='+str(student_id))
	if student_id:
		local_paths = get_local_course_paths(student_id)
		remote_paths = get_remote_course_paths(student_id)
		if local_paths and remote_paths:
			ret = copy_files(local_paths, remote_paths)
	log_message('copy_local_to_remote exit')
	return ret

def get_remote_course_paths(student_id):
	log_message('get_remote_course_paths enter')
	log_message('get_remote_course_paths student_id='+str(student_id))
	remote_base_file_path = os.path.join(BASE_REMOTE, student_id)
	remote_course_paths = get_course_paths(remote_base_file_path, student_id)
	log_message('get_remote_course_paths exit')
	return remote_course_paths

def get_local_course_paths(student_id):
	log_message('get_local_course_paths enter')
	log_message('get_local_course_paths student_id='+str(student_id))
	local_base_file_path = BASE_LOCAL
	local_course_paths = get_course_paths(local_base_file_path, student_id)
	log_message('get_local_course_paths exit')
	return local_course_paths

def internet_on():
	log_message('internet_on enter')
	ret = 0
	try:
		response = urllib2.urlopen('https://www.dropbox.com', timeout=4)
		log_message("internet_on response " + str(response))
	except:
		ret = -1
		log_message('internet_on failed!')
		log_error()
	log_message('internet_on exit')
	return ret

def restart_dropbox():
	log_message('restart_dropbox enter')
	ret = 0
	try:
		subprocess.call(['dropbox', 'stop'])
		subprocess.call(['dropbox', 'start'])
	except:
		ret = -1
		log_message('restart_dropbox failed!')
		log_error()
	log_message('restart_dropbox exit')
	return ret

def main():
	import time
	t = time.strftime('%X %x %Z')
	log_message('submit_course.py started at ' + str(t))
	msg = 'submit course completed successfully'
	ret = 0
	# ret = internet_on()
	if ret == -1:
		msg = 'submit course failed (no internet connection)'
	else:	
		ret = 0
		# ret = restart_dropbox()
		if ret == -1:
			msg = 'submit course failed (cannot sync)'
		else:
			ret = copy_local_to_remote()
			if ret == -1:
				msg = 'submit course failed (cannot copy)'	
	log_message('submit_course.py returned ' + str(ret))
	gui = TinkerAcademyMessage(msg)
	gui.show()

if __name__ == "__main__":
	main()