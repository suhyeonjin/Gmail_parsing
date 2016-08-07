# -*- encoding: cp949 -*-
#use to folium // not use google maps
import folium
import os

#drowing map class
class drow_map():
	def drow_GPS(self, gps_list,today_directory):#, file_name_l):
		print "[=]", today_directory
		if today_directory == 'total':
			os.chdir("..\\")

		else:
			os.chdir(today_directory)
		#print os.getcwd()
		if gps_list[0][0] == 'null':
			lat_long = 37,39
		else:lat_long = gps_list[0]
		
		#open file, first you'll see this place
		map_2 = folium.Map(location=lat_long,zoom_start=1)
		lat_lon = gps_list

		#and, markered any place! it has gps data
		draw_list = []
		for k in range(len(lat_lon)):
			#print '[+]',lat_lon[k]
			i,j = lat_lon[k]
			if i == 'null' or j == 'null':
				continue
			map_2.simple_marker([i,j],marker_icon = 'cloud',popup=str(i)+", "+str(j)+'_GPS_palce')

			print "[*] Important_GPS.. : ",i,j,k
			draw_list.append([i,j])

		print "[+] Drawing GPS..."
		
		print "now directory :", os.getcwd()
		if os.path.exists("./GPS_drow.html"):
			print "EXIST!!"
			os.remove("./GPS_drow.html")
		
		map_2.line(draw_list,  line_color='#FF0000', line_weight=5)
		map_2.save(outfile="GPS_drow.html")
		
		#map_2.create_map(path='GPS_drow.html')