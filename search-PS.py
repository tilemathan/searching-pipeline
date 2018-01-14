#!/usr/bin/env python
"""
External packages ******************************************
"""
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

"""
**************** SEARCH PARAMETERS **************************
"""
min_pulse_period = 0.001 #sec  (for Camillo method)

"DEDISPERSION"
dmlistpath = "/u/tilemath/bin/pipeline2017/DMlists/dmlist200.txt"

"""
*************************************************************
"""
dmlist = []
dm = []
def reader(filename):
	"GLOBAL STRINGS: telescope, machine, source_name"
	global telescope
	telescope = subprocess.check_output("header %s -telescope" % (filename), shell=True)
	global machine
	machine = subprocess.check_output("header %s -machine" % (filename), shell=True)
        global source_name

	if (telescope == "Fake\n"):  #if the file is fake we use another source_name because the default is huge and has gaps
		source_name = "Fake"
	else:	
		source_name = subprocess.check_output("header %s -source_name" % (filename), shell=True)

	"GLOBAL FLOATS: fch1, foff, nchans, tstart, tsamp, nbits, nifs, headersize, datasize, nsamples"
	global fch1
	fch1_string = subprocess.check_output("header %s -fch1" % (filename), shell=True)
        fch1 = float(fch1_string)
	global foff
	foff_string = subprocess.check_output("header %s -foff" % (filename), shell=True)
        foff = float(foff_string)
	global nchans
	nchans_string = subprocess.check_output("header %s -nchans" % (filename), shell=True)
        nchans = int(nchans_string)
	global tstart
	tstart_string = subprocess.check_output("header %s -tstart" % (filename), shell=True)
        tstart = float(tstart_string)
	global tsamp
	tsamp_string = subprocess.check_output("header %s -tsamp" % (filename), shell=True)
        tsamp = float(tsamp_string)
	global nbits
	nbits_string = subprocess.check_output("header %s -nbits" % (filename), shell=True)
        nbits = int(nbits_string)
	global nifs 
	nifs_string = subprocess.check_output("header %s -nifs" % (filename), shell=True)
        nifs = int(nifs_string)
	global headersize
	headersize_string = subprocess.check_output("header %s -headersize" % (filename), shell=True)
        headersize = int(headersize_string)
	global datasize
	datasize_string = subprocess.check_output("header %s -datasize" % (filename), shell=True)
        datasize = int(datasize_string)
	global nsamples
	nsamples_string = subprocess.check_output("header %s -nsamples" % (filename), shell=True)
        nsamples = int(nsamples_string)
	global tobs
	tobs_string = subprocess.check_output("header %s -tobs" % (filename), shell=True)
        tobs = float(tobs_string)

def calc(filename, P_orb_str, WD_mass_str, Min_mass_str):
	"""
	**************** BINARY PARAMETERS **************************
	"""
	global P_orb #days
	global P_orb_sec
	global WD_mass #solar masses
	global Min_mass #solar massses

	P_orb = float(P_orb_str)	#convert sting variables to floats
	WD_mass = float(WD_mass_str)
	Min_mass = float(Min_mass_str)	

	"AC range and step calculation"
	global ACmax
	global ACmin
	global ACstep
	c = 2.99E8               #m/s
        T = 4.925490947E-6       #s in order the masses to be in solar units
        GM = 1.327124400E+11
	P_orb_sec  = P_orb*24*60*60
	
	Omega_orb = 2*math.pi/(P_orb_sec)
	a_R =(c*(T*(Min_mass+WD_mass))**(0.333333333))/Omega_orb**0.666666667
	a_p = a_R*(WD_mass/(Min_mass+WD_mass))
	a=a_p*Omega_orb**2
        ACmax = a_p*Omega_orb**2
        ACmin = -a_p*Omega_orb**2

	"Camilo method"
        #ACstep = c*min_pulse_period/(tobs**2) 
        "Lyne/Eatough method"
        ACstep = 64*c*(tsamp*10**(-6))/(tobs**2)
	
def DM(filename, workdir):
	os.chdir(workdir)
	global dmlist
	global dm
	print "Dedispersion and zerodming"
	dedmea = open(dmlistpath, "r")
	effdmlist = dedmea.readlines
	i=0
	for item in dedmea:
		dmi = float(item)
		dmlist.append(dmi)
		if dmlist[i]<120: #zerodm methon doesnt work good below DM = 120
			os.system('dedisperse %s -d %s  > DM%s.tim' % (filename, dmlist[i], dmlist[i]))
		else:
			os.system('dedisperse %s -subzero -d %s  > DM%s.tim' % (filename, dmlist[i], dmlist[i])) #-subzero
			#os.system('dedisperse_all %s -d %s -zerodm > DM%s.tim' % (filename, dmlist[i], dmlist[i]))
		i=i+1
	dedmea.close()
	
def search(filename, workdir):
	os.chdir(workdir)
	os.system('step %s %s %s > aclist' % (ACmin, ACmax, ACstep))
	dedmea = open(dmlistpath, "r")
	i=0
	for item in dedmea:
		print "Searching..."
		os.system('my_accn DM%s' % (dmlist[i]) )  #acceleration search with my_accn
		#os.system('seek DM%s.tim -z -fftw' % (dmlist[i])) # -z option is for the birdies
		i=i+1
	os.system('cat DM*.prd > all.prd')
	os.system('cp %s/all.prd %s/all.prd' % (workdir, resultdir) )
	os.chdir(resultdir)
	print "Finding best candidates..."
	os.system('/hercules/u/tilemath/bin/pipeline2017/condense_try.py -f all.prd -s 10')
        os.system('/hercules/u/tilemath/bin/pipeline2017/pulsarhunter/scripts/ph-best all.prd.condensed-SN10.prd cands')
	print "Procedure Completed."

"""**************** MAIN PROGRAM *************************"""

def main(workdir, resultdir, filename):
	reader(filename)
	calc(filename, P_orb_str, WD_mass_str, Min_mass_str)
	DM(filename, workdir) 
	search(filename, workdir)
	print "Search completed."

"""*******************************************************"""
if __name__ == "__main__":
	workdir = sys.argv[1]
   	resultdir = sys.argv[2]
	filename = sys.argv[3]
	P_orb_str = sys.argv[4] #days
	WD_mass_str = sys.argv[5] #solar masses
	Min_mass_str = sys.argv[6] #solar masses
	main(workdir, resultdir, filename)
