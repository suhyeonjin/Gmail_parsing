from PIL import Image
from PIL.ExifTags import GPSTAGS,TAGS
import exifread

class get_GPS():
	def get_exif_data(self,imageFile):
		print "[+] GPS_path....",imageFile

		image = Image.open(imageFile)
		
		exif_data = {}
		info = image._getexif()
		if info:
			for tag, value in info.items():
				decoded = TAGS.get(tag, tag)
				if decoded == "GPSInfo":
					gps_data = {}
					for t in value:
						sub_decoded = GPSTAGS.get(t, t)
						gps_data[sub_decoded] = value[t]

					exif_data[decoded] = gps_data
				else:
					exif_data[decoded] = value

		return exif_data

	def _get_if_exist(self,data, key):
		if key in data:
			return data[key]
			
		return None
		
	def _convert_to_degress(self, value):
		
		d0 = value[0][0]
		d1 = value[0][1]
		d = float(d0) / float(d1)

		m0 = value[1][0]
		m1 = value[1][1]
		m = float(m0) / float(m1)

		s0 = value[2][0]
		s1 = value[2][1]
		s = float(s0) / float(s1)

		return d + (m / 60.0) + (s / 3600.0)

	def get_lat_lon(self,exif_data):
		lat = None
		lon = None
#		print exif_data

		if "GPSInfo" in exif_data:		
			gps_info = exif_data["GPSInfo"]
#			print '[+]',gps_info['GPSLatitude'][0]
#			print '[+]',gps_info['GPSLongitude']

			gps_latitude = self._get_if_exist(gps_info, "GPSLatitude")
#			print gps_latitude

			gps_latitude_ref = self._get_if_exist(gps_info, "GPSLatitudeRef")
			gps_longitude = self._get_if_exist(gps_info, "GPSLongitude")
			gps_longitude_ref = self._get_if_exist(gps_info, "GPSLongitudeRef")

#			print 'ww',gps_latitude_ref

		
			if gps_latitude and gps_latitude_ref and gps_longitude and gps_longitude_ref:
				lat = self._convert_to_degress(gps_latitude)
#				print '!',lat
				if gps_latitude_ref != "N":                     
					lat = 0 - lat

				lon = self._convert_to_degress(gps_longitude)
				if gps_longitude_ref != "E":
					lon = 0 - lon
			
						
		return (round(lat,4), round(lon,4))

#jpeg GPS
#imgFile = './img/1445426254403.jpeg'
#g = get_GPS()
#g1 = g.get_exif_data(imgFile)
#print g.get_lat_lon(g1)

