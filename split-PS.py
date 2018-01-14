#!/usr/bin/env python

import glob
import os
import os.path
import shutil
import socket
import struct
import sys
import time
import subprocess
import warnings
import re
import types
import tarfile
import tempfile
import numpy as np
import math

def partitions(sourcename):
	#tsamp = 54.61333
	PART = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J']
	os.chdir('/hercules/u/tilemath/PILOT-SURVEY-SPLIT')
	#tpass=0
	for i in range(0,10):
		os.system('mkdir /hercules/u/tilemath/PILOT-SURVEY-SPLIT/%s_%s' % (sourcename, PART[i]))
		#copy birdies file and paste to SPLIT folder
		os.system('cp /hercules/u/tilemath/PILOT-SURVEY-DATA/%s/birdies_%s /hercules/u/tilemath/PILOT-SURVEY-SPLIT/%s_%s/birdies_%s' % (sourcename, sourcename, sourcename, PART[i], sourcename))
	start=0
	for beam in range(0,7):
		for i in range(0,10):
			#nlength=int(458/(tsamp/(10**6)))
			#npass=int(tpass/(tsamp/(10**6)))
			#end=npass+nlength
			duration=8386230
			os.chdir('/hercules/u/tilemath/PILOT-SURVEY-SPLIT/%s_%s' % (sourcename, PART[i]))
			os.system('SplitFil.py /hercules/u/tilemath/PILOT-SURVEY-DATA/%s/%s_0%s_8bit.fil %s %s %s_0%s_%s.fil' % (sourcename, sourcename, beam, start, duration, sourcename, beam, PART[i]))
			#tpass=tpass+458
			start=start+8386230
			os.chdir('/hercules/u/tilemath/PILOT-SURVEY-SPLIT')
		start=0

if __name__ == "__main__":
	sourcename = sys.argv[1]
	partitions(sourcename)
