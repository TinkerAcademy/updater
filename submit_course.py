#!/usr/bin/python

import os
import uuid
import sys
import syslog
import tinkeracademy
from tinkeracademy import read_student_id
from tinkeracademy import copy_files
from tinkeracademy import get_course_paths
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
			ret = copy_files(local_paths, remote_paths, True)
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

def main():
	import time
	t = time.strftime('%X %x %Z')
	log_message('submit_course.py started at ' + str(t))
	ret = copy_local_to_remote()
	log_message('submit_course.py returned ' + str(ret))
	if ret == -1:
		gui = TinkerAcademyMessage('submit course failed')
		gui.show()
	else:
		gui = TinkerAcademyMessage('submit course completed successfully')
		gui.show()

if __name__ == "__main__":
	main()