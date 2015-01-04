#!/usr/bin/python

###############################################################################
#
#   Fix It Script
#
#   Copyright Tinker Academy 2014
###############################################################################

import os
import subprocess
from tinkeracademy import log_message
from tinkeracademy import log_error

BASE_REMOTE= '/home/tinkeracademystudent/Dropbox/classes/scripts'

FIX_IT_FILES = [
	# os.path.join(BASE_REMOTE,'reset_submit.py'),
	# os.path.join(BASE_REMOTE,'fix_odt.py'),
	# os.path.join(BASE_REMOTE,'reset_minecraft.py')
]

def main():
	for file_ in FIX_IT_FILES:
		log_message('fix_it ' + str(file_))
		subprocess.call(['python', file_])

if __name__ == "__main__":
	main()