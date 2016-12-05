#!/usr/local/bin/python
########################################
#python: 2.7.3
#author: shenlay
#date:2013-03-01
#version:0.0.4
########################################
import pysvn # http://pysvn.tigris.org/
import getopt, sys, time, string
sys.path.append('/var/www/uper/pythonc/lib')


import smtplib,time
from email.MIMEText import MIMEText
import passwd,urllib
import os, urllib2,re
from urlparse import urlparse
from hashlib import md5
import datetime,argparse


#Config Svn
months = time.strftime("%m",time.localtime())
days = time.strftime("%d",time.localtime())
years = time.strftime("%Y",time.localtime())
username = "xxx"
password = "xxxxxxx"
argv = sys.argv
upcount = []
path = "/Down_Codes"
url = "svn://xxxxxxxxxx:7654/repos_web/"



#Config CDN
cdnuser = "xxxxxxx"
cdnpass = "xxxxxx"
apiurl  = "http://xxxxxxxxxx:8080/wsCP/servlet/contReceiver?"





'''try:
	versions = argv[1]
except:
	print "<font color='#ff3300'>Error:  Please Input The Normal Version.</font>"
	exit(1)'''




parser = argparse.ArgumentParser(description="\
								 version 0.0.4",
                                 epilog="If You Hava Some Questions, Please Mail To xxxx",
                                 prefix_chars="-",
                                 formatter_class=
                                 argparse.ArgumentDefaultsHelpFormatter)






parser.add_argument("-v",
                    "--version",
                    nargs="*",
#					type=int,
					dest="versions",
					default=[],
					help="Svn Numbers With Granter Than 1,Please Separated By   ,  ")
parser.add_argument("-d",
                    "--domain",
                    nargs="*",
#					type=int,
					dest="cdomain",
					default=[],
					help="Cleaning Up The Templates_C Directory (Smarty's Cache Directory)")
parser.add_argument("-mail",
                    "--mail",
                    nargs="*",
                    default=[],
#					type=int,
					dest="mailuser",
					help="If It Seted, Will Mail To The User Or Will Be Not")
parser.add_argument("-cdns",
                    "--cdns",
                    nargs="*",
#					type=int,
					dest="cdns",
					default=[],
					help="Purge The Caches For The Domains With CDN's API")
parser.add_argument("-cfile",
                    "--cfile",
                    nargs="*",
                    default=[],
#					type=int,
					dest="cfile",
					help="Through CDN Cache Interface To Clean Up Those Files")
parser.add_argument("-cdir",
                    "--cdir",
                    nargs="*",
                    default=[],
#					type=int,
					dest="cdir",
					help="Through CDN Cache Interface To Clean Up Those Directories")
parser.add_argument("-V",
                    dest="%(prog)s versions",
                    action="version",
                    version="%(prog)s 0.0.4")

try:
	args = parser.parse_args()
	versions = ",".join(args.versions)
	mailuser = "".join(args.mailuser).split(",")
	cdomain = args.cdomain
	cdns = args.cdns
	cfile = args.cfile
	cdir = args.cdir
#	print cdns
#	exit(11)


except Exception,e:
	print "<font color='#ff3300'>Error:check the argparse arguments %s </font>" %(e)
	exit(-1)


#print "cdomain:%s" %(cdomain)
#print "versions:%s" %(versions)
#print mailuser
#exit(1)





######################################################################################
#Send The Publish Result To The Users
#The Best Mail Is 139 or qq
#Smtp Server Is xxxx
######################################################################################

def send_mail(to_list,sub,content):
	mail_host="xxxxx"
	mail_user="aa@xxxxxx"
	mail_postfix=" "
	mail_pass="xxxxxx"
	me="Uploader"+"<"+mail_user+"@"+mail_postfix+">"
	msg = MIMEText(content,_subtype='plain',_charset='gb2312')
	msg['Subject'] = sub
	msg['From'] = me
	msg['To'] = ";".join(to_list)
	try:
		server = smtplib.SMTP()
		server.connect(mail_host)
		server.login(mail_user,mail_pass)
		server.sendmail(me, to_list, msg.as_string())
		server.close()
		return True
	except Exception, e:
		print str(e)
	return False



#####################################################################################
#Login The Svn Server
#Return Authentication Information.
#####################################################################################

def get_login( realm, user, may_save ):
	return True, username, password, False




######################################################################################
#Getting The Codes From Svn Server,Only Through Svn Nums
#Three Types:
#          ***
#          deleted files
#          added  files
#          charged files
#          ***
#####################################################################################

def getting(i):
	#url = unicode(url, sys.stdin.encoding)
	#winpath = path.replace('\\','\\\\')
	try:
		num = i
		targetpath = path+"/"+str(years)+"/"+str(months)+"/"+str(days)+"/"+str(num)
		last_num = num - 1
		revision = pysvn.Revision(pysvn.opt_revision_kind.number, num )
		last_revision = pysvn.Revision(pysvn.opt_revision_kind.number, last_num)
		client = pysvn.Client()
		if(username != "" and password != ""):
			client.callback_get_login = get_login
		summary = client.diff_summarize(url, last_revision, url, revision)
	except:
		print "<font color='#ff3300'>svn version is not exist or svn_server is not connected by you.</font><br>"
	try:
		for changed in summary:
			if(pysvn.diff_summarize_kind.delete == changed['summarize_kind']):
				delpath = changed['path']
				dellist.append(delpath)
			#print "del list: %s" %(dellist)
			if(pysvn.diff_summarize_kind.added == changed['summarize_kind']):
				changepath = changed['path']
				addlist.append(changepath)
				if(changed['node_kind'] == pysvn.node_kind.file):
					file_text = client.cat(url+urllib.quote(changed['path'].encode('utf8')), revision)
					fullPath = targetpath+"/"+changed['path']
					dirPath = fullPath[0:fullPath.rfind("/")]
					if not os.path.exists(dirPath):
						os.makedirs(dirPath)
					f = open(fullPath,'wb')
					f.write(file_text)
					f.close
			#print "add list: %s" %(addlist)
			elif(pysvn.diff_summarize_kind.modified == changed['summarize_kind']):
				modifipath = changed['path']
				modifilist.append(modifipath)
				if(changed['node_kind'] == pysvn.node_kind.file):
					file_text = client.cat(url+urllib.quote(changed['path'].encode('utf8')), revision)
					fullPath = targetpath+"/"+changed['path']
					dirPath = fullPath[0:fullPath.rfind("/")]
					if not os.path.exists(dirPath):
						os.makedirs(dirPath)
					f = open(fullPath,'wb')
					f.write(file_text)
					f.close
			#print "modifi list: %s" %(modifilist)

	except:
		print "<font color='#ff3300'>svn getfiles failse, please check the svn_server and the network, sure the permission of the %s</font><br>" %(targetpath)
		raise ValueError("getting error....")
		return False
	else:
		return True

###########################################################################################
#Throuth '' getting '' Fuction Download The Codes
#Multi-Versions
###########################################################################################

def mergeget():
	global dellist
	global addlist
	global modifilist
	global ver_lit
	dellist = []
	addlist = []
	modifilist = []
	ver_lit = versions.split(',')
	try:
		for i in ver_lit:
			i = int(i)
			'''if(i <= 0):
				print "<font color='#ff3300'>versions must > 0,thanks.</font>"
				return False
			else:'''
			getting(i)
	except Exception,e:
		print "<font color='#ff3300'>all the input is exception...  %s</font><br>" %(e)
		exit(-1)
	#print("<font color='#ff3300'>Input Exception, Version Num Must > 0 And Is A Valid Version More Than Two Versions Separated By   ,  </font>")
	#return False
	result = "<html><body> <b>Del_Files:</b><br><font size='' color='#ff0000'>%s</font> <hr><b>Add_Files:<br></b> <font size='' color='#cc9900'>%s </font><hr><b>Modified_Files:<br></b> <font size='' color='#006600'>%s</font></html></body><br><br><br><br>" % ('<br>'.join(dellist), \
                                                                                                                                                                                                                                                               '<br>'.join(addlist), '<br>'.join(modifilist))
	print result
	return True

#############################################################################################
#Build The Change File List 
#Delete All The Cache On CDNs Of A Domain
#Through The WANGSU's API Purge The Static Cache
#Http API
#############################################################################################



def cdnfile(domain):
	global upcount,cdnuser,cdnpass,apiurl
	all_change = dellist + addlist + modifilist
	upcount.append(domain)
	if(upcount.count(domain) == 1):
		#print "all chagrging is : %s <br>" %(all_change)
		hashlist = []
		newhashlist = []
		for i in all_change:
			furl = re.search(domain+".*",i)
			if(furl):
				hashlist.append(furl.group())
		#print hashlist
		#print cdnuser+cdnpass+";".join(hashlist)
		for i in hashlist:
			i = re.sub('a.com','b.com',i)
			newhashlist.append(i)
		hashvalue = md5(cdnuser+cdnpass+";".join(newhashlist)).hexdigest()
		requesturl = apiurl+"username="+cdnuser+"&passwd="+hashvalue+"&url="+";".join(newhashlist)
		try:
			resource = urllib2.urlopen(requesturl)
			print "<font color='#F00078'> %s </font><br>" %(requesturl)
			print "<font color='#F00078'>[ %s ] CDN Result: %s </font><br>" %(domain,resource.read())
		except Exception ,e:
			print "<font color='#ff3300'>Open The API %s  Exception: %s</font><br>"  %(apiurl,e)
			exit(-1)




############################################################################################
#Uploading The Codes .
#Calling The Shell Scripts And Using Ncftp Tools In The Command Modal.
#But Del Files With The Lftp Tools
############################################################################################

def ftpuper():
	#list_path = "/var/www/uper/pythonc/cdn/file.list"
	#webserver IP address
	webhost = passwd.webhost
	loginhost = passwd.loginhost
	bbshost = passwd.bbshost
	weplayhost = passwd.weplayhost
	adhost = passwd.adhost
	#The domain-name and ftp password
	webdomain = passwd.webdomain
	bbsdomain = passwd.bbsdomain
	weplaydomain = passwd.weplaydomain
	logindomain = passwd.logindomain
	addomain = passwd.addomain
	allresult = []

#if(os.path.getsize(list_path) != 0):
#		del_hf = open(list_path,'w')
#		del_hf.close()



	for x in ver_lit:
		codepath = path+"/"+str(years)+"/"+str(months)+"/"+str(days)+"/"+str(x)
		longfile = os.popen("find %s  -type f |head -1" % (codepath)).read()
		domain_match = re.search("xxxx|aaaa|bbbbb|ccccc|dddd",longfile,re.I)
		if(domain_match):
			for k in webdomain:
				matchs = re.search("\/"+k,longfile,re.I)
				if(matchs):
					updir_web = re.sub(k+".*",k,longfile)
					upuser = webdomain[k].keys()
					upuser_str = ''.join(upuser)
					uppasswd = webdomain[k][upuser_str]
					#cdnfile  count the charged files
					try:
						run = os.system("/var/www/uper/pythonc/shell/ncftp.sh %s %s %s %s"  %(upuser_str,uppasswd,webhost,updir_web))
						if(run == 0):
							result = "user: %s <br>domain: %s <br>version: %s<br>host: %s<br>dir: %s<br><font color='#33cc00'>...Upload Success!</font><hr>" %(upuser_str,k,x,webhost,updir_web)
							allresult.append(result)
							cdnfile(k)
						else:
							result = "<font color='#ff3300'>user: %s <br>domain: %s <br>version: %s<br>host: %s<br>dir: %s<br>Error: - %s _ %d <br>See the shell scripts...</font><hr>" %(upuser_str,k,x,webhost,updir_web,k,run)
							allresult.append(result)
					except:
						print " web Error: Time Out or An Exception Arises,Please Retry. <br>If You Don't Know How To Resolve, Please Mail To: rayshen@3388.com Or Phone:110120."
			for j in bbsdomain:
				matchs = re.search("\/"+j,longfile,re.I)
				if(matchs):
					updir_bbs = re.sub(j+".*",j,longfile)
					upuser = bbsdomain[j].keys()
					upuser_str = ''.join(upuser)
					uppasswd = bbsdomain[j][upuser_str]
					#cdnfile(j)
					try:
						run = os.system("/var/www/uper/pythonc/shell/ncftp.sh %s %s %s %s"  %(upuser_str,uppasswd,bbshost,updir_bbs))
						if(run == 0):
							result = "user: %s <br>domain: %s <br>version: %s<br>host: %s<br>dir: %s<br><font color='#33cc00'>...Upload Success!</font><hr>" %(upuser_str,j,x,bbshost,updir_bbs)
							allresult.append(result)
						else:
							result = "<font color='#ff3300'>user: %s <br>domain: %s <br>version: %s<br>host: %s<br>dir: %s<br>Error: - %s _ %d <br>See the shell scripts...</font><hr>" %(upuser_str,j,x,bbshost,updir_bbs,j,run)
							allresult.append(result)
					except:
						print "bbs Error: Time Out or An Exception Arises,Please Retry. <br>If You Don't Know How To Resolve, Please Mail To: rayshen@3388.com Or Phone:110120."
			for q in weplaydomain:
				matchs = re.search("\/"+q,longfile,re.I)
				if(matchs):
					updir_we = re.sub(q+".*",q,longfile)
					upuser = weplaydomain[q].keys()
					upuser_str = ''.join(upuser)
					uppasswd = weplaydomain[q][upuser_str]
					#cdnfile(q)
					try:
						run = os.system("/var/www/uper/pythonc/shell/ncftp_hk.sh %s %s %s %s"  %(upuser_str,uppasswd,weplayhost,updir_we))
						if(run == 0):
							result = "user: %s <br>domain: %s <br>version: %s<br>host: %s<br>dir: %s<br><font color='#33cc00'>...Upload Success!</font><hr>" %(upuser_str,q,x,weplayhost,updir_we)
							allresult.append(result)
						else:
							result = "<font color='#ff3300'>user: %s <br>domain: %s <br>version: %s<br>host: %s<br>dir: %s<br>Error: - %s _ %d <br>See the shell scripts...</font><hr>" %(upuser_str,q,x,webhost,updir_we,q,run)
							allresult.append(result)
					except:
						print "weplay Error: Time Out or An Exception Arises,Please Retry. <br>If You Don't Know How To Resolve, Please Mail To: rayshen@3388.com Or Phone:110120."
			for n in logindomain:
				matchs = re.search("\/"+n,longfile,re.I)
				if(matchs):
					updir_login = re.sub(n+".*",n+"/trunk",longfile)
					upuser = logindomain[n].keys()
					upuser_str = ''.join(upuser)
					uppasswd = logindomain[n][upuser_str]
					#cdnfile(n)
					try:
						run = os.system("/var/www/uper/pythonc/shell/ncftp.sh %s %s %s %s"  %(upuser_str,uppasswd,loginhost,updir_login))
						if(run == 0):
							result = "user: %s <br>domain: %s <br>version: %s<br>host: %s<br>dir: %s<br><font color='#33cc00'>...Upload Success!</font><hr>" %(upuser_str,n,x,loginhost,updir_login)
							allresult.append(result)
						else:
							result = "<font color='#ff3300'>user: %s <br>domain: %s <br>version: %s<br>host: %s<br>dir: %s<br>Error: - %s _ %d <br>See the shell scripts...</font><hr>" %(upuser_str,n,x,webhost,updir_login,run)
							allresult.append(result)
					except:
						print "login Error: Time Out or An Exception Arises,Please Retry. <br>If You Don't Know How To Resolve, Please Mail To: rayshen@3388.com Or Phone:110120."
			for p in addomain:
				matchs = re.search("\/"+p,longfile,re.I)
				if(matchs):
					updir_web = re.sub(p+".*",p,longfile)
					upuser = addomain[p].keys()
					upuser_str = ''.join(upuser)
					uppasswd = addomain[p][upuser_str]
					#print updir_web
					#print upuser_str
					#print uppasswd
					try:
						run = os.system("/var/www/uper/pythonc/shell/ncftp.sh %s %s %s %s"  %(upuser_str,uppasswd,adhost,updir_web))
						if(run == 0):
							result = "user: %s <br>domain: %s <br>version: %s<br>host: %s<br>dir: %s<br><font color='#33cc00'>...Upload Success!</font><hr>" %(upuser_str,p,x,adhost,updir_web)
							allresult.append(result)
							cdnfile(p)
						else:
							result = "<font color='#ff3300'>user: %s <br>domain: %s <br>version: %s<br>host: %s<br>dir: %s<br>Error: - %s _ %d <br>See the shell scripts...</font><hr>" %(upuser_str,p,x,adhost,updir_web,p,run)
							allresult.append(result)
					except:
						print " web Error: Time Out or An Exception Arises,Please Retry. <br>If You Don't Know How To Resolve, Please Mail To: rayshen@3388.com Or Phone:110120."
		else:
			result = "<font color='#ff3300'>Error: Only Support __Domain__  Linekong.com|3388.com|Weplaygame.com.my|bbs.3388/lklk.com|login_union<br>Please Sure The Version Num Include These Domains..</font>"
			print result



	#all_updir = [updir_web,updir_bbs,updir_we,updir_login]
	all_result =  "\n".join(allresult)
	print all_result
	if(mailuser != ['']):
		send_mail(mailuser,"Codes Publishing Report",all_result)

	return True




#####################################################################################################
#Clean The Templates_c Directory
#Is Smarty's Cache
#####################################################################################################
def clean(servername,dir):
	webhost = passwd.webhost
	webdomain = passwd.webdomain
	webhost = passwd.webhost
	servername = "".join(servername)
	if(servername in webdomain.keys()):
		upuser = webdomain[servername].keys()
		upuser_str = ''.join(upuser)
		uppasswd = webdomain[servername][upuser_str]
		#print "%s==>%s===>%s===>%s" %(webhost,upuser_str,uppasswd,dir)
		try:
			run = os.system("/var/www/uper/pythonc/shell/clean_cache.sh %s %s %s %s %s"  %(webhost,upuser_str,uppasswd,dir,servername))
			if(run == 0):
				result = "<font color='#33cc00'>...Cleaning Success ==>  %s</font>" %(servername)
				print result
			else:
				result = "<font color='#ff3300'>...Cleaning False ==>  %s</font><br>error:%d" %(servername,run)
				print result
		except:
			print "<font color='#ff3300'>Cleaning The %s==>%s Is Errors ...</font>" %(servername,dir)
	else:
		print "<font color='#ff3300'>%s is not exist... thanks</font><br>" %(servername)





#########################################################################################################
#Through The API To Clean Up The CDN Cache
#
#Two Types:
#            1> Clean Up Files
#            2> Clean Up Directories
#            3> "/" Is Meaning: Clean Up All The Cache Of A Site.
#
#########################################################################################################
def purge(pdomain,pfile,pdir):
	try:
		global upcount,cdnuser,cdnpass,apiurl
		cdnflist = []
		cdndlist = []
		if(len(pfile) != 0 and len(pdir) == 0):
			#Default Is List, Charge To The Format
			pfile_list = "".join(pfile).split(";")
			for i in pfile_list:
				cdnflist.append("".join(pdomain)+i)

			smd5 = ";".join(cdnflist)
			smd5value = md5(cdnuser+cdnpass+smd5).hexdigest()
			purgeurl = apiurl+"username="+cdnuser+"&passwd="+smd5value+"&url="+smd5
			purgeresult = urllib2.urlopen(purgeurl).read()
			print "=========================================================================================================<br>"
			print "Purge Domain: %s <br>"  %(pdomain)
			print "Purge Files: %s <br>"  %(smd5)
			print "Purge Result: <font color='#33cc00'> %s</font> <br><br><br><br> Purge The Cache Need Take A While ...(2-3 Minutes)<br>" \
			%(purgeresult)
			print "=========================================================================================================<br>"
			'''print smd5
			print smd5value
			print purgeurl
			print purgeresult'''


		elif(len(pfile) == 0 and len(pdir) != 0):
			pdir_list = "".join(pdir).split(";")
			for i in pdir_list:
				cdndlist.append("".join(pdomain)+i)

			smd5 = ";".join(cdndlist)
			smd5value = md5(cdnuser+cdnpass+smd5).hexdigest()
			purgeurl = apiurl+"username="+cdnuser+"&passwd="+smd5value+"&dir="+smd5
			purgeresult = urllib2.urlopen(purgeurl).read()
			print "=========================================================================================================<br>"
			print "Purge Domain: %s <br>"  %(pdomain)
			print "Purge Directories: %s <br>"  %(smd5)
			print "Purge Result: <font color='#33cc00'> %s</font> <br><br><br><br> Purge The Cache Need Take A While ...(2-3 Minutes)<br>" \
			%(purgeresult)
			print "=========================================================================================================<br>"
			'''print smd5
			print smd5value
			print purgeurl
			print purgeresult'''


		elif(len(pfile) != 0 and len(pdir) != 0):
			pfile_list = "".join(pfile).split(";")
			for i in pfile_list:
				cdnflist.append("".join(pdomain)+i)

			#At The Same Time Clean Up The Files And Directories
			pdir_list = "".join(pdir).split(";")
			for i in pdir_list:
				cdndlist.append("".join(pdomain)+i)

			smd5 = ";".join(cdnflist) + ";".join(cdndlist)
			smd5value = md5(cdnuser+cdnpass+smd5).hexdigest()
			purgeurl = apiurl+"username="+cdnuser+"&passwd="+smd5value+"&url="+";".join(cdnflist)+"&dir="+";".join(cdndlist)
			purgeresult = urllib2.urlopen(purgeurl).read()
			print "=========================================================================================================<br>"
			print "Purge Domain: %s <br>"  %(pdomain)
			print "Purge Files And Directories: %s <br>"  %(smd5)
			print "Purge Result: <font color='#33cc00'> %s</font> <br><br><br><br> Purge The Cache Need Take A While ...(2-3 Minutes)<br>" \
			%(purgeresult)
			print "=========================================================================================================<br>"
			'''print smd5
			print smd5value
			print purgeurl
			print purgeresult'''
	except Exception,e:
			print "<font color='#ff3300'>CDN Purge Error:  %s</font><br>" %(e)





#The Main
if(__name__ == '__main__'):
	#main_args = ['versions','cdomain','cdns']
	#for i in main_args:
	if(versions):
		mergeget()
		ftpuper()
	elif(cdomain):
		clean(cdomain,"templates_c")
	elif(cdns):
		purge(cdns,cfile,cdir)















