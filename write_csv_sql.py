# -*- coding: utf-8 -*-
import csv
import sqlite3
import os
import urllib2

#write csv file,,,
#data_ is input datas...
class csv_write():
	def __init__(self):
		os.chdir('..\\')
		
		#Create result save DB and make Table Query and Auto commit setting
		self.conn = sqlite3.connect("./result.db")
		self.conn.text_factory = str
		self.conn.isolation_level = None							
		self.conn.executescript("CREATE TABLE IF NOT EXISTS Parsing (Number INTEGER PRIMARY KEY AUTOINCREMENT, NAME TEXT, Time TEXT, Shorted_URL TEXT, Full_URL TEXT, MD5 TEXT, SHA1 TEXT, GPS_lat TEXT, GPS_lon TEXT)")
		

	#query setting fuction, INSERT work
	def query_db(self, query, args=(), one=False):
		global conn
		cur = self.conn.execute(query, args)
		if query.strip()[:6].upper() == 'INSERT':
			rv = cur.lastrowid
		else:
			rv = cur.fetchall()
		self.conn.commit()
		cur.close()		
		return (rv[0] if rv else None) if one else rv


	#write csv file and query database
	def input_data(self, sql_data, today_directory):#,data_):
		print "\n\n"
		#print "[+] SQL_Query_Data_\n",sql_data
		matrix = []
		
		#if you want create for day database, thie code work
		#os.chdir(today_directory)
		os.chdir(today_directory)
		
		#write csv file open
		f = open("./result.csv","wb")
		cw = csv.writer(f , delimiter=',', quotechar='|')
		
		#write title
		cw.writerow(["No.1","Name","Time","Shorted Url","Full_Url","MD5","SHA1","GPS(lat)","GPS(lon)"])

		#[sql_data[i],sql_data[i+1],sql_data[i+2],sql_data[i+3],sql_data[i+4],sql_data[i+5],sql_data[i+6],sql_data[i+7],sql_data[i+8]]
		
		#write csv file, query sql data, items important!
		for i in range(len(sql_data)):
			#sql_data[i][1] = urllib2.unquote(sql_data[i][1]).decode('utf-8').encode('cp949')
			cw.writerow([i+1,sql_data[i][1].encode('euc-kr'),sql_data[i][2],sql_data[i][3],sql_data[i][4],sql_data[i][5],sql_data[i][6],sql_data[i][7],sql_data[i][8]])

			#number table was integer auto increat setting, Query database
			self.query_db(
					'INSERT INTO Parsing ( NAME, Time, Shorted_URL, Full_URL,MD5,SHA1, GPS_lat, GPS_lon  ) VALUES (?,?,?,?,?,?,?,?)',
					([sql_data[i][1].encode('utf-8'),sql_data[i][2],sql_data[i][3],sql_data[i][4],sql_data[i][5],sql_data[i][6],sql_data[i][7],sql_data[i][8]])
				)
			print "[*] query_data : ",[i,sql_data[i][1].encode('euc-kr'),sql_data[i][2],sql_data[i][3],sql_data[i][4],sql_data[i][5],sql_data[i][6],sql_data[i][7],sql_data[i][8]],"\n"

		f.close()

		return self.conn.execute("SELECT gps_lat, gps_lon from parsing;").fetchall()
		#self.read_data()
		
	#Read and print CSV file// input, file path, name,,, and read data of csv file
	'''
	def read_data(self):
		f = open('./result.csv','r')
		matrix = []
		csvReader = csv.reader(f)
		for row in csvReader:
			matrix.append(row)
			print row
		f.close()
	'''