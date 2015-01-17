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

def poweroff():
	try:
		ps = subprocess.Popen(('echo', 'tinker2015'), stdout=subprocess.PIPE)
		ps2 = subprocess.Popen(('sudo', '-S', 'poweroff'), stdin = ps.stdout, stdout=subprocess.PIPE)
		output = ps2.communicate()[0]
		if output:
			print output
		ps.stdout.close()
	except:
		print 'error poweroff'

def main():
	poweroff()

if __name__ == "__main__":
	main()