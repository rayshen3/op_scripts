#!/usr/bin/env  python
#encoding:utf-8


#######################################################################
#date:    2013-06-28                                                  #
#author:  shenlay                                                     #
#version: 0.0.1                                                       #
#######################################################################

import MySQLdb as mdb
import sys

reload(sys)
sys.setdefaultencoding('utf-8')


########################################################################
class MyDb():
	"""Just A Simple Class Of Mysql DataBase

	"""

	def __init__(self,host="localhost",user="root",passwd=None,port=None,db=None,charset="utf8"):
		'''Get The Server Connet Info'''
		self.host = host
		self.user = user
		self.port = port
		self.passwd = passwd
		self.charset = charset
		self.db = db
		self.char = charset

	def connet(self):
		'''Connet The Db Server'''
		try:
			self.conn = mdb.connect(host=self.host,user=self.user,passwd=self.passwd,db=self.db,port=self.port,charset=self.char)
			self.cur = self.conn.cursor()
			#print self.cur
		except Exception,e:
			print "Can't Connet The db Server: %s  %s" %(self.host,e)

	def selectdb(self,dbname):
		'''Select Db'''
		try:
			self.dbname = dbname
			self.conn.select_db(dbname)
		except Exception,e:
			print "No Found DataBase: %s %s"  %(self.dbname,e)

	def executesql(self,sql):
		'''Run Common Sql Orders, Like: show tables; show varibles like "%temp%"
        Also Can Be Used To Query Data
		'''
		try:
			#self.cur.execute('SET NAMES utf8')
			self.cur.execute(sql)
			exec_res = []
			for i in self.cur.fetchall():
				_res = map(lambda x:str(x),i)
				exec_res.append(_res)
			return exec_res
		except Exception,e:
			print "Sql Execute Error: %s %s" %(sql,e)



#test = MyDb(host="192.168.0.106",passwd="redhat",port=3306,db="pdb")
#test.connet()
#test.selectdb('pdb')
#result =test.executesql("show variables like '%join%'")
#print result

