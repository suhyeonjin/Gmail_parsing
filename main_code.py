# -*- coding: utf-8 -*-
import gmail
import re
import base64
import httplib
import urlparse
import urllib2
import urllib
import ssl
import datetime
from datetime import timedelta
import os
import operator

#get data customize class import 
from get_gps import *
from get_faceCount import *
from draw_gps import *
from get_hash_file import *
from write_csv_sql import *


#unshort_url
def unshorten_url(url):
	parsed = urlparse.urlparse(url)
	h = httplib.HTTPConnection(parsed.netloc)
	h.request('HEAD', parsed.path)
	response = h.getresponse()
	if response.status/100 == 3 and response.getheader('Location'):
		return response.getheader('Location')
	else:
		return url

#get_orginal url
def get_url(url,referer):		
	try:#http connect
		if "https" in url:
#			opener = urllib2.build_opener(urllib2.HTTPSHandler(context=ssl.SSLContext(ssl.PROTOCOL_SSL23)))
#			urllib2.install_opener(opener)
			print "	[+] SSL."

		#url set
		req = urllib2.Request(url)
		req.add_header("User-agent","Mozilla/5.0")
		req.add_header("Referer",referer)
		response = urllib2.urlopen(req)
		url_ = response.geturl()
		#print "[+] full_url : ",url_
	except IOError, e:
		print "	[+] url error"
		return 0
	return url_

#get url_file data
def get_source(url,referer):
	try:		
		if "https" in url:
			#opener = urllib2.build_opener(urllib2.HTTPSHandler(context=ssl.SSLContext(ssl.PROTOCOL_SSL23)))
			#urllib2.install_opener(opener)
			print "	[+] SSL."

		req = urllib2.Request(url)
		req.add_header("User-agent","Mozilla/5.0")
		req.add_header("Referer",referer)
		response = urllib2.urlopen(req)
		the_page = response.read()
	
	except IOError, e:
		print "	[+] url error"
		return 0
	
	return the_page

#base64decode_ 
def my_base64_decode(data):
	decode_data = False
	if bool(re.match(r"^[A-Za-z0-9+\/=]+$", data)) == False:
		return False
	try:
		decode_data = base64.b64decode(data)
	except:
		decode_data = False

	return decode_data

#get_mail_data, text,  befor parsing
def get_mail(date_,g):
	mail_dic = {}
	send_time_l=[]

	year_, month_, day_ = date_
	print '[+]',year_, month_, day_ 

	#except url list manage dic
	#dic_ = {'http://me2.do/xWbrYn85':'https://osint.xyz/bob/whereami.jpg','http://me2.do/5gCPJlT0':'https://osint.xyz/bob/%EC%9A%B0ahh%ED%95%98ga(우ahh하ga).jpg','http://me2.do/xWbrYn85':'https://osint.xyz/bob/whereami.jpg','https://goo.gl/kjhof3':'https://osint.xyz/bob/Whyjpg'}
	dic_ = {'https://goo.gl/kjhof3':'https://osint.xyz/bob/Why...jpg'}

	#read_mail user setting
	unread = g.inbox().mail(sender='Sender_email', on = datetime.date(int(year_), int(month_), int(day_)))
	#unread = g.label("Forensic").mail(before=datetime.date(int(year_b),int(month_b),int(day_b)+1))

	i = 1
	result_data = []

	#Read mail from sender
	for newmail in unread:
		result = ''
		newmail.fetch()
		print "[+] mail title : ",i," : ",newmail.subject
		i += 1
		
		#get send_time
		send_time = newmail.sent_at
		send_time += timedelta(hours=9)
		send_time = str(send_time)+' UTC+9'
		print "[+] send time : ",send_time
		send_time_l.append(send_time)

		#mail Text get & base64 en, decoding
		try: 
			mail_text = str(unicode(newmail.body)).strip()
			mail_data = mail_text
		except:
			mail_data =  str(newmail.body).strip()

		mail_data = mail_data.replace('\n', '').replace("\r", '').strip()
		decode_data = my_base64_decode(mail_data)
		if decode_data:
			print "[+] mail_data : ",decode_data.decode('utf-8').encode('cp949').strip()
			result_data.append(str(decode_data.decode('utf-8').encode('cp949').strip()))
		else:
			print "[+] mail_data  : ",mail_data.strip()
			result_data.append(str(mail_data.strip()))
	

		mail_dic[''.join(result_data[-1:])] = send_time
		print 
		

	#mail_item, time
	sort_mail_dic = sorted(mail_dic.items(),key=operator.itemgetter(1))
	#print sort_mail_dic

	
	#get read mail, and Body url parsing
	reg_url = re.compile(r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+\/[0-9a-zA-Z]+')
	
	#full_url
	result_url_ = []
	
	#short_url
	before_url_l = []
	
	#total_mails >> result_data
	for i in result_data:
		url_ = reg_url.findall(str(i))[0]
		print "[+] Short_url. : ",url_
		
		url_ = ''.join(url_)
		url_ori = url_

		while True:
			if url_ == '':
				print "[-] NOT exist URL"
				print
				break

			#extension check
			#print unshorten_url(url_)[-4:], unshorten_url(url_)
	
			###except url 
			try:
				if dic_[url_]:
					print "[+] Full_url : ",dic_[url_]
					print
					result_url_.append(dic_[url_])
					before_url_l.append(url_)
					break
			except:
				pass

			#check download url correct
			if '.jpg' == unshorten_url(url_)[-4:] or '.JPG' == unshorten_url(url_)[-4:] or '.pdf' == unshorten_url(url_)[-4:] or '.PDF' == unshorten_url(url_)[-4:]:
				#print unshorten_url(url_)[-4:]
				print "[+] Full_url : ",unshorten_url(url_)
				print
				result_url_.append(unshorten_url(url_))
				before_url_l.append(url_)
				break
			else:
				url_ = url_[:-1]
				if url_[-1] == '/':
					url_ = url_ori
					url_ = unshorten_url(url_)
					if '.jpg' == get_url(url_,url_)[-4:] or '.JPG' == get_url(url_,url_)[-4:] or '.pdf' == get_url(url_,url_)[-4:] or '.PDF' == get_url(url_,url_)[-4:]:
						print "[+] Full_url : ", get_url(url_,url_)
						print
						result_url_.append(get_url(url_,url_))
						before_url_l.append(url_)
				#	else:
				#		print "[+] Full_url(not jpg, pdf) :",dic_[url_]
				#		print
				#		result_url_.append(dic_[url_])
				#		before_url_l.append(url_)
						
					break
			
	#return full, short url , send time
	return result_url_, send_time_l, before_url_l
	

if __name__ == "__main__":
	#get today
	#Today = str( datetime.date.today())#.split('-')
	Today = raw_input('input date parse mail start ex) 2016-07-07 : ')
	date_= str(Today).split('-')
	flag = 1

	#default_directory set
	xml_path = os.path.dirname( os.path.abspath( __file__ ) )
	default_directory = os.path.dirname( os.path.abspath( __file__ ) )+'\\result\\'
	if os.path.isdir(default_directory) == False:#directory 가 존재하지 않으면
		os.mkdir(default_directory)
		os.chdir(default_directory)
	else:
		os.chdir(default_directory)
	
	today_directory = default_directory+str(Today)

	#check directory before make directory
	if os.path.isdir(today_directory) == False:#directory 가 존재하지 않으면
		os.mkdir(today_directory)
		os.chdir(today_directory)
	else:
		os.chdir(today_directory)

	
	#gmail login and get session
	g = gmail.login('ID', 'PW') # input your gmail id & pw
	try:
		if g.logged_in:
			print('Mail log in success')
		g.logout	   
	except:
		#could not login
		gmail.AuthenticationError
		print('log in fail')


	try:
		#get mail important return from get_mail!!
		result_url_, send_time_l, before_url_l = get_mail(date_,g)

	except IOError, e:
		pass

	print "\n=============Result_data==================="
	print "[+] Short_url_list : ",before_url_l
	print "[+] Full_url_list : ",result_url_
	print "[+] Send_time_list : ",send_time_l
	print "\n\n"
	#send time list recieve
	gps_l = []
	file_name_l = []
	hash_l = []
	default_directory = os.path.dirname( os.path.abspath( __file__ ) )

	url_ = result_url_

	#download_url_file
	for url1 in url_:
		print "\n\n[+] File_download : ",url1
		#temp url_except
		if "https://125.131.189.45/" in url1 :
			url1 = url1.replace('https://125.131.189.45/','https://osint.xyz/')
			print url1
		url_data = get_source(url1,url1)
		
		#filename parsing and file download
		filename_ = url1.split('/')[-1]
		filename_ = urllib2.unquote(filename_).decode('utf-8')
		print "		[+] download_file_name : ",filename_
#		filename_ = filename_.decode('utf-8').encode('cp949')
		file_name_l.append(filename_)

		#file true or False
		if os.path.exists(filename_):
			print "[+] Exist_file! "
			f = open(filename_,'wb')
			f.write(url_data)
			f.close()
		
		else:
		#file write
			f = open(filename_,'wb')
			f.write(url_data)
			f.close()

		#file download_path & filename
		file_down =  str(os.getcwd())+'\\'+filename_
		
		print "[+] File_Path! : ",file_down
		
		#get_GPS important & true file check
		if '.jpg' in file_down or '.JPG' in file_down or '.jpeg' in file_down:
			try:
				gps_Data = get_GPS()
				exif_data = gps_Data.get_exif_data(file_down)
				gps_l.append(list(gps_Data.get_lat_lon(exif_data)))
				print "[+] lat & lon : ",gps_l[-1:]
				#True Flase flag Set
				flag=1
				
			except:
				#gps data is null
				gps_l.append(('null','null'))
				print "[+] not JPG"
				flag = 0
				pass

		else:
			#gps data is null
			gps_l.append(('null','null'))
			print "[+] not JPG"
			flag = 0
		
		#file hash get
		hash_f = hash_get()
		hash_l.append(hash_f.get_hash(file_down))
		print "[+] Hash  : ",hash_l[-1:]

		
		#count Face print used OpenCV
		try:
			if flag == 0:
				continue
			face_count = Count_face()
			Face_cnt = face_count.cnt(file_down, xml_path)
			print "[+] people_count : ",Face_cnt
		
		except:
			print "[+] Error, Not Found Face!!!"

		#go to default directory
		os.chdir(default_directory)

	#check not exist email
	if len(url_) == 0:
		quit()
		
	#drow_gps_ in the map
	print "\n\n[*] Drowing_map...."
	Dg = drow_map()
	Dg.drow_GPS(gps_l,today_directory)
	
	#set the SQL_Query total data
	#All important list reference
	print "[*] Query_SQL..."
	SQL_data = []
	for i in range(len(send_time_l)):
		SQL_data.append([i,file_name_l[i], send_time_l[i], before_url_l[i], result_url_[i], hash_l[i][0], hash_l[i][1], gps_l[i][0], gps_l[i][1]])

	#queryed SQL, CSV write
	sql_ = csv_write()
	#get_total_gps_list in Query!
	result_query = sql_.input_data(SQL_data,today_directory)
	total_gps_l=[]

	for i in result_query:
		if i == ('null','null'):
			continue
		else:
			temp = (float(i[0]), float(i[1]))
			total_gps_l.append(temp)
	
	print "[+] Drowing_total_map...."
	Dg.drow_GPS(total_gps_l,"total")
	print "[+] Finished" 
