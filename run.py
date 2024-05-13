# from dataLoader import dataLoader
# from evaluation import evaluator
from objectDetection import visDrone


m = visDrone.VisDroneModel(device="cpu")


import cv2 
import numpy as np 
  
# Create a VideoCapture object and read from input file 
cap = cv2.VideoCapture('test_video.mp4') 
  
# Check if camera opened successfully 
if (cap.isOpened()== False):
    print("Error opening video file") 
res = []
img = cv2.imread("testss/frame0001.png")
h,w,_ = img.shape

video=cv2.VideoWriter('video_res.avi',-1,20,(w,h))
# Read until video is completed 
count = 0
while(cap.isOpened()): 
      
# Capture frame-by-frame 
    ret, frame = cap.read() 
    if ret == True: 
    # Display the resulting frame 
        #cv2.imshow('Frame', frame)
        result,_ = m.predictImage(frame)
        #print(result)
        res.append(result)
        video.write(result)
        cv2.imwrite("testss/video/frame%d.png" % count, result)
    # Press Q on keyboard to exit 
        if cv2.waitKey(25) & 0xFF == ord('q'): 
            break
        count += 1
# Break the loop 
    else: 
        break
  
# When everything done, release 
# the video capture object 
cap.release() 

cv2.destroyAllWindows()
video.release()
# d = Displayer(item=146,nframe=27)
# d.show()
# # d = Displayer()
# # d.show()
# # rembg

# d = dataLoader.Displayer()
# d.show()

# e = evaluator.Eval()
# e.newEval("public/images/ski_new.png")


# pp = e.getNextObj()
# e.showImage()
# e.showGaussianDiff()
# pp = e.getNextObj()
# e.showImage()

# vp = visDrone.VisDroneModel(device="cpu")
# predict,boxes = vp.predictImage("public/images/ski.png")
# vp.showImage(predict)
