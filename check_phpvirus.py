#/usr/bin/env python
#coding: utf-8
#Used To Check The Webshell,  PHP Files.
#By rayshen

import os,sys,re
import datetime,time
import smtplib
from email.mime.text import MIMEText

#dt = str(now.year)+"-"+str(now.month)+"-"+str(now.day)+" "+str(now.hour)+":"+str(now.minute)+":"+str(now.second)
#before_time = now - datetime.timedelta(hours = 1)
#before_time_new = before_time.strftime('%Y-%m-%d %H:%M:%S.%f')
#unixtime = time.mktime(time.strptime(before_time.strftime('%Y-%m-%d %H:%M:%S.%f'),'%Y-%m-%d %H:%M:%S.%f'))
#print  before_time_new

now = datetime.datetime.now()
dt = now.strftime("%Y-%m-%d %H:%M:%S")
filetype = ['.php']
mail_host = "smtp.163.com"
mail_user = "xxxx@163.com"
mail_pass = "xxx"
mail_postfix = "ll.com"
mailto_list = ['xxxx@ll.com']
logpath = "C:\\Python27\\check.log"
logfile = open(logpath,'a+')
argv = sys.argv
argc = len(argv)
file_count = 0
virusnum = 0
keyword = {"c99":"base64_encode\(ob_get_contents|bindport","r57":"r57shell|port_bind_bd_c","0x00PHPshell":"0x00.ath.cx|blacklight",\
        "0xshell":"63a9f0ea7bb98050796b649e85481845|login_0xShell","andr3a92shell":"andr3a92|evilcode_base64","ctshell":"ctftpbrutecheck|ctfsearch",\
        "StresBypassshell":"Mohajer22|BiyoSecurityTeam","SnIpEr_SAshell":"\\x50\\x4b\\x05\\x06\\x00\\x00\\x00\\x00|datapipe_c",\
        "SimAttacker":"WWW.SIMORGH-EV.COM|id=fm&fdownload=","phpRemoteView":"c=base64&c2=0|phpRemoteView","NSTshell":"fastcmd()|sh311",\
        "NetworkFileManagerPHP":"final_english_release|csvdumptable","Mysqlinterface":"mysql_web_admin_username|action=viewSchema&dbname=",\
        "iron_shell":"www.ironwarez.info|spawn_shell","gnyshell":"TVqQAAMAAAAEAAAA|GNY.Shell","DxShell":"26.04.2006|DxMODES",\
        "webadmin":"Reddragonfly|r_admin\[admin\]","phpspy2011":"encode_pass\(|secinfo","phpspy2008":"phpspypass|goaction\(\'backconnect",\
        "phpspy2006":"Version:2006|proxycontents","phpspytrans":"7Zt/TBNnGMf|action=mysqlfun","EasyPHPWebShell":"EasyPHPWebShell|smy_password",\
        "PH4ckP":"$xY7_test|getinfo\(\$xy7\)"}

if(argc < 2):
	print "Check Webshell Tools\nVersion:0.0.1\n\nError: \nUsage: %s [targetdir]   \ne.g.  %s /usr/local/php" %(argv[0],argv[0])
	exit(1)
else:
	phpdir = argv[1]

def send_mail(to_list,sub):
	mail_file = open(logpath,'rb')
	mail_content = mail_file.read()
	me="Py_Checker"+"<"+mail_user+"@"+mail_postfix+">"
	msg = MIMEText(mail_content,_subtype='plain',_charset='gb2312')
	msg['Subject'] = sub
	msg['From'] = me
	msg['To'] = ";".join(to_list)
	try:
		server = smtplib.SMTP()
		server.connect(mail_host)
		server.login(mail_user,mail_pass)
		server.sendmail(me, to_list, msg.as_string()
		server.close()
		return True
        except Exception, e:
		print str(e)
		return False
	finally:
		mail_file.close()

def checkfile(filename):
	global virusnum
	hf = open(filename,'r')
	content = hf.read()
	for key in keyword.keys():
		matchs = re.search(keyword[key],content,re.I)
		if(matchs):
			virusnum += 1
			#result = matchs.group()
			searchlog = "%s %s: VirusName:%s VirusLabel:%s\n" %(dt,filename,key,keyword[key])
			#print >> logfile,matchs
			logfile.write(searchlog)
	hf.close()

	return None

def checkalldir(dirpath):
	global file_count
	try:
		filelist = os.listdir(dirpath)
	except:
		print >> logfile,dt+" "+dirpath+" Permission Deny"
		#print "%s %s Permission Deny\n" %(dt,dirpath)
	else:
		for i in filelist:
			abspath = dirpath+"\\"+i
			if(os.path.isdir(abspath)):
				try:
					checkdir(abspath)
				except:
					print "%s %s Permission Deny\n" %(dt,dirpath)
			elif(os.path.isfile(abspath)):
				#print >> logfile,abspath
				filename = os.path.basename(abspath)
				postfix = os.path.splitext(filename)[1]
				if(postfix in filetype):
					file_count += 1
					checkfile(abspath)

	return None
def checkmatchdir(dirpath):
	global file_count
	try:
		filelist = os.listdir(dirpath)
	except:
		print >> logfile,dt+" "+dirpath+" Permission Deny"
		#print "%s %s Permission Deny\n" %(dt,dirpath)
	else:
		for i in filelist:
			abspath = dirpath+"\\"+i
			if(os.path.isdir(abspath)):
				try:
					checkdir(abspath)
				except:
					print "%s %s Permission Deny\n" %(dt,dirpath)
			elif(os.path.isfile(abspath)):
				#print >> logfile,abspath
				filename = os.path.basename(abspath)
				postfix = os.path.splitext(filename)[1]
				if(postfix in filetype):
					file_count += 1
					filemt = time.localtime(os.stat(abspath).st_mtime)
					filetime = datetime.datetime( filemt[0] ,filemt[1] ,filemt[2], filemt[3], filemt[4], filemt[5], filemt[6])
					diffsecond = (now-filetime).seconds
					if(diffsecond <= 60*60):
						checkfile(abspath)

	return None

def main():
	if(int(os.path.getsize(logpath)) == 0):
		checkalldir(phpdir)
	else:
		checkmatchdir(phpdir)

	print >> logfile,"%s All Check Files: %d" %(dt,file_count)
	if(virusnum == 0):
		print >> logfile,"%s All The Files Normal! \n" %(dt)
	else:
		print >> logfile,"%s VirusNum: %d\n" %(dt,virusnum)
		logfile.close()
		send_mail(mailto_list,"phpcheck_test")


	return True

if(__name__=="__main__"):
	main()

