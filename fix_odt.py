#!/usr/bin/python

###############################################################################
#
#   Fix Quiz Files
#
#   Copyright Tinker Academy 2014
###############################################################################

import os
import uuid
import sys
import syslog
import subprocess
import shutil
import urllib2
import re
import tinkeracademy
from tinkeracademy import read_student_id
from tinkeracademy import get_course_paths
from tinkeracademy import log_message
from tinkeracademy import log_error
from tinkeracademy import TinkerAcademyMessage
from tinkeracademy import TinkerAcademyConfirmDialog
from tinkeracademy import TinkerAcademyMessage

BASE_LOCAL='/home/tinkeracademystudent/Documents/tinkeracademy/Courses'

def close_all_running_instances():
	log_message('close_all_running_instances enter')
	proc = subprocess.Popen(['ps', '-ef'], stdin=subprocess.PIPE, \
		stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
	line = proc.stdout.readline()
	success = True
	while True:
		if not line or line == '':
			break
		if re.search("libreoffice", line):
			success = False
			request_close_libreoffice()
			break
		line = proc.stdout.readline()
	proc.stdin.close()
	proc.stdout.close()
	if success:
		do_actual_remove_odt_files()
	log_message('close_all_running_instances exit')

def request_close_libreoffice():
	msg = 'Close LibreOffice And Run "Fix It" Again!'
	gui = TinkerAcademyMessage(msg)	
	gui.show()

def do_actual_remove_odt_files():
	student_id = read_student_id()
	local_path = BASE_LOCAL
	relative_file_paths = get_relative_file_paths_in_dir(local_path)
	rm_file_list = []
	for relative_file_path in relative_file_paths:
		if os.path.splitext(relative_file_path)[1].lower() == '.odt':
			file_path = os.path.join(local_path, relative_file_path)
			dir_path = os.path.dirname(file_path)
			file_paths = os.listdir(dir_path)
			for file_path in file_paths:
				if re.search("\.\~lock\..*\.odt\#", file_path):
					full_file_path = os.path.join(dir_path, file_path)
					rm_file_list.append(full_file_path)
	for rm_file in rm_file_list:
		log_message(' removing file ' + rm_file)
		subprocess.call(['rm', '-rf', rm_file])
	msg = 'No files had to be fixed! You can restart LibreOffice now.'
	if len(rm_file_list) > 0:
		msg = str(len(rm_file_list)) + ' files had to be fixed!. You can restart LibreOffice now.'
	gui = TinkerAcademyMessage(msg)	
	gui.show()

def get_relative_file_paths_in_dir(dir_path):
	log_message('get_relative_file_paths_in_dir enter')
	relative_file_paths = []
	for root, dirs, files in os.walk(dir_path):
		rel_root = root.replace(dir_path, '')
		if rel_root and len(rel_root) > 0:
			if rel_root[0] == '/':
				rel_root = rel_root[1:]
			if rel_root:
				for file_ in files:
					relative_file_path = os.path.join(rel_root, file_)
					# log_message('get_relative_file_paths_in_dir adding relative_file_path=' + str(relative_file_path))
					relative_file_paths.append(relative_file_path)
	log_message('get_relative_file_paths_in_dir exit')
	return relative_file_paths

def remove_locks_on_odt_files():
	close_all_running_instances()

def confirm_fix_odt_files():
	log_message('confirm_fix_odt_files enter')
	msg = 'Do you need to fix any of the quiz files?'
	gui = TinkerAcademyConfirmDialog(msg, remove_locks_on_odt_files)
	gui.show()
	log_message('confirm_fix_odt_files exit')

def main():
	confirm_fix_odt_files()	

if __name__ == "__main__":
	main()