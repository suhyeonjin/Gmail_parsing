#use OPEN CV to face count
import cv2
import numpy as np

#get_face_count class
class Count_face:
	def cnt(self,imgFile, xml_path):
		
		print "[+]",xml_path
		print "[+] imgfile : ",imgFile

		#xml file is learning data file, face and eyes
		faceCascade = cv2.CascadeClassifier(xml_path+'\\xml\\haarcascade_frontalface_default.xml')
		eyeCascade = cv2.CascadeClassifier(xml_path+'\\xml\\haarcascade_eye.xml')
		image = cv2.imread(imgFile)
		gray = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

		#face count setting from learning data XML file
		faces = faceCascade.detectMultiScale(
			gray,
			scaleFactor=1.1,
			minNeighbors=5,
			minSize=(30, 30),
			flags = 0#cv2.cv.CV_HAAR_SCALE_IMAGE
		)

		#check the face_count from Image and draw Rectangle!!
		for (x, y, w, h) in faces:
			cv2.rectangle(image, (x, y), (x+w, y+h), (0, 255, 0), 2)
			eyes = eyeCascade.detectMultiScale(gray)
			for (ex,ey,ew,eh) in eyes:
				cv2.rectangle(image,(ex,ey),(ex+ew,ey+eh),(0,255,0),2)
				
		#Popup check image and to do exit next check
		cv2.imshow("Faces found", image)
		cv2.waitKey(0)
		
		return len(faces)

#Check code
#face_count = Count_face()
#print face_count.cnt('./img/people.PNG','D:\\BOB\\Report\\wonyoung\\parsing\\')