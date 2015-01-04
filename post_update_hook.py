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
from tinkeracademy import log_message
from tinkeracademy import log_error
from tinkeracademy import TinkerAcademyMessage

BASE_LOCAL='/home/tinkeracademystudent/Documents/tinkeracademy/Setup'

BASE_REMOTE= '/home/tinkeracademystudent/Dropbox/classes/scripts'

# def setup_fix_it_link():
#  	log_message('setup_fix_it_link enter')
#  	target_file = BASE_REMOTE
#  	target_file = os.path.join(target_file, 'fix_it.py')
#  	target_file = os.path.abspath(target_file)
#  	link_file = BASE_LOCAL
#  	link_file = os.path.join(link_file, 'Fix It')
#  	subprocess.call(['rm', '-f', link_file])
#  	subprocess.call(['ln', '-s', target_file, link_file])
#  	log_message('setup_fix_it_link exit')

def update_submit():
	file_=os.path.join(BASE_REMOTE,'update_submit.py')
	subprocess.call(['python', file_])

def run_post_update_hook():	
	# setup_fix_it_link()
	update_submit()
