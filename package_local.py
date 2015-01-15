#!/usr/bin/python

import os
import uuid
import sys
import syslog
import subprocess
import urllib2
import errno
import shutil
import zipfile
import tinkeracademy
from tinkeracademy import get_relative_file_paths_in_dir
from tinkeracademy import log_message
from tinkeracademy import log_error
from tinkeracademy import TinkerAcademyMessage

COURSE_PACKAGES = {
	'TA-SCR-1': {
		'CourseName' : 'TA-SCR-1',
		'CourseDescription' : 'SCRATCH Programming Adventure (TA-SCR-1)',
		'CourseFileName': 'SCRATCH Programming Adventure.zip',
		'CourseContent' : {
			'handout' : [ 'handout1', ],
			'homework': [ 'homework1', ],
			'quiz' : [ 'quiz0', 'quiz1', ],
			'starterpack': [ 'starterpack1', ],
		},
	},
	'TA-JAV-1': {
		'CourseName' : 'TA-JAV-1',
		'CourseDescription' : 'Programming Using Java (TA-JAV-1)',
		'CourseFileName': 'Programming Using Java.zip',
		'CourseContent' : {
			'handout' : [ 'handout1', ],
			'homework': [ 'homework1', ],
			'quiz' : [ 'quiz0', 'quiz1', ],
			'starterpack': [ 'starterpack1', ],
		},
	},
	'TA-JAV-2': {
		'CourseName' : 'TA-JAV-2',
		'CourseDescription' : 'AP Computer Science Prep (Java Programming) (TA-JAV-2)',
		'CourseFileName': 'AP Computer Science Prep (Java Programming).zip',
		'CourseContent' : {
			'handout' : [ 'handout1', ],
			'homework': [ 'homework1', ],
			'quiz' : [ 'quiz0', 'quiz1', ],
			'starterpack': [ 'starterpack1', ],
		},
	},
	'TA-JAV-3': {
		'CourseName' : 'TA-JAV-3',
		'CourseDescription' : 'AP Computer Science Prep (Java Data Structures & Algorithms) (TA-JAV-3)',
		'CourseFileName': 'AP Computer Science Prep (Java Data Structures & Algorithms).zip',
		'CourseContent' : {
			'handout' : [ 'handout1', ],
			'homework': [ 'homework1', ],
			'quiz' : [ 'quiz0', 'quiz1', ],
			'starterpack': [ 'starterpack1', ],
		},
	},
}

CONFIG_BASE='/Users/rvergis/Dropbox/classes/config'
TARGET_CONFIG_BASE = 'config'
SCRIPTS_BASE='/Users/rvergis/Dropbox/classes/scripts'
TARGET_SCRIPTS_BASE = 'scripts'
COURSES_BASE='/Users/rvergis/Dropbox/classes/courses'
TARGET_COURSES_BASE = 'courses'
TARGET_BASE='/Users/rvergis/Documents/tinkeracademy/git/website/tinkeracademy/static'
TARGET_TEMP_BASE='/Users/rvergis/Documents/tinkeracademy/git/website/tinkeracademy/static/_tmp'

def package_local():
	log_message('package_local enter')
	# cleanup
	for packagename in COURSE_PACKAGES:
		course = COURSE_PACKAGES[packagename]
		cleanup_local(course)
	create_tmp()
	copy_common_tmp()
	for packagename in COURSE_PACKAGES:
		course = COURSE_PACKAGES[packagename]
		cleanup_local(course)
		copy_course_tmp(course)
		package_tmp(course)
		cleanup_course_tmp(course)
	cleanup_tmp()
	log_message('package_local exit')

def cleanup_local(course):
	log_message('cleanup_local enter')
	target_file_name = course['CourseFileName']
	target_file_name = os.path.join(TARGET_BASE, target_file_name)
	if os.path.isfile(target_file_name):
		os.remove(target_file_name)
	else:
		print target_file_name, ' does not exist '
	log_message('cleanup_local exit')
	return True

def create_tmp():
	log_message('create_tmp enter')
	mkdirs(TARGET_TEMP_BASE)
	log_message('create_tmp exit')

def copy_common_tmp():
	log_message('copy_common_tmp enter')
	files_to_copy = []
	target_dirs = []
	files_to_copy.append(SCRIPTS_BASE)
	target_dirs.append(os.path.join(TARGET_TEMP_BASE, TARGET_SCRIPTS_BASE))
	files_to_copy.append(CONFIG_BASE)
	target_dirs.append(os.path.join(TARGET_TEMP_BASE, TARGET_CONFIG_BASE))
	for i in range(len(files_to_copy)):
		file_to_copy = files_to_copy[i]
		target_dir = target_dirs[i]
		pdir = os.path.dirname(target_dir)
		mkdirs(pdir)
		shutil.copytree(file_to_copy, target_dir)
	log_message('copy_common_tmp enter')

def copy_course_tmp(course):
	log_message('copy_tmp enter')
	files_to_copy = []
	target_dirs = []
	coursename = course['CourseName']
	coursecontents = course['CourseContent']
	for contentkey in coursecontents:
		contents = coursecontents[contentkey]
		for content in contents:
			content_path = os.path.join(COURSES_BASE, coursename, contentkey, content)
			files_to_copy.append(content_path)
			target_dirs.append(os.path.join(TARGET_TEMP_BASE, TARGET_COURSES_BASE, coursename, contentkey, content))
	for i in range(len(files_to_copy)):
		file_to_copy = files_to_copy[i]
		target_dir = target_dirs[i]
		pdir = os.path.dirname(target_dir)
		mkdirs(pdir)
		shutil.copytree(file_to_copy, target_dir)
	log_message('copy_tmp exit')
	return True

def package_tmp(course):
	target_file_name = course['CourseFileName']
	target_file_name = os.path.join(TARGET_BASE, target_file_name)
	zipped = zipfile.ZipFile(target_file_name, 'w', zipfile.ZIP_DEFLATED)
	filelist = get_relative_file_paths_in_dir(TARGET_TEMP_BASE)
	for file_ in filelist:
		zipped.write(os.path.join(TARGET_TEMP_BASE, file_), file_)

def cleanup_course_tmp(course):
	coursename = course['CourseName']
	target_dir = os.path.join(TARGET_TEMP_BASE, TARGET_COURSES_BASE, coursename)
	shutil.rmtree(target_dir)

def cleanup_tmp():
	shutil.rmtree(TARGET_TEMP_BASE)

def mkdirs(path):
    try:
        os.makedirs(path)
    except OSError as exc:
        if exc.errno == errno.EEXIST and os.path.isdir(path):
            pass
        else: 
        	raise
def main():
	import time
	t = time.strftime('%X %x %Z')
	log_message('package_local.py started at ' + str(t))
	msg = 'package local completed'
	ret = package_local()
	if ret == -1:
		msg = 'package local failed'
	log_message('package_local.py returned ' + str(ret))
	print msg

if __name__ == "__main__":
	main()