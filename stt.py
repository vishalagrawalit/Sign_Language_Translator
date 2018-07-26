import speech_recognition as sr
import cv2
import os


image_folder = "images"
video_name = "demo.avi"


r = sr.Recognizer()

harvard = sr.AudioFile("harvard.wav")
with harvard as source:
    audio = r.record(source)

text = r.recognize_google(audio, show_all=True)
text = text["alternative"][0]["transcript"]

images = [img for img in os.listdir(image_folder) if img.endswith(".jpg")]
print(images)


frame = cv2.imread(image_folder + "/" + images[ord(text[0].upper())-65], 0)
cv2.imshow('video', frame)
height, width  = frame.shape

# Define the codec and create VideoWriter object
fourcc = cv2.VideoWriter_fourcc(*'mp4v') # Be sure to use lower case
video =  cv2.VideoWriter(video_name, fourcc, 20.0, (width, height))


for i in range(1, len(text)):
	if 65<= ord(text[i].upper()) <=90:
		frame = cv2.imread(image_folder + "/" + images[ord(text[i].upper())-65], 0)
		video.write(frame)
    
video.release()

cv2.destroyAllWindows()

print("The video is made.")

'''
Quality of idea
Team members
scalibilty
Revenue
innovation
additional
'''