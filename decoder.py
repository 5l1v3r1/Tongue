# -*- coding: utf-8 -*-   
import time,Image   
import os, win32gui, win32ui, win32con, win32api   

from ftplib import FTP
import sys
import zipfile

import time

import string

import logging

import socket
	
	
from zipfile import ZipFile
if __name__ == '__main__':
	if len(sys.argv) != 2:
		print "wrong : need mac address!"
		exit(0)
	p1 =  str(sys.argv[1]).replace("-","")
	p1 = p1[-3:]
	filenames = []
	for root,dirs,files in os.walk("./"):
		for filename in files:
			if ".zip" in filename:
				filename = filename.replace(".zip","")
				filenames.append(filename)
	if len(filenames) ==0 :
		print "there is no zip file!"
		exit(0)
	for cell in filenames:
		ppp = cell.replace("-","")
		ppp = ppp[-4:]
		p = p1 + ppp
		rootdir =  os.path.abspath("./")
		command =rootdir +'/tools/zip.exe x -p'+p+' '+'*.zip ./'
		print "[*]"+str(os.popen(command))
		time.sleep(5)
	print "all work completed!"
	#print filenames