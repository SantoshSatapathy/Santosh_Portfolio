#!/usr/bin/env python
# coding: utf-8

# In[28]:


# CIS*6020: Artificial Intelligence
# Assignment 2
# Student: Santosh Kumar Satapathy
# Under the guidance of Dr. Neil Bruce

# makenonogram.py

# We will use the cv2 library for image processing
import cv2  
from matplotlib import pyplot as plt
import numpy as np  
import pandas as pd
  
image1 = cv2.imread('original image 1.tiff')  
# image2 = cv2.imread('/kaggle/input/ec22222/Einstein copy.tiff')  

# Convert the image in grayscale  
img = cv2.cvtColor(image1, cv2.COLOR_BGR2GRAY) 

# Reduce the pixels to scale down and generate and solveable nonogram. In case of Image1, we are reducing the image to 2% of its original size
scale_percent = 2 # percent of original size
width = int(img.shape[1] * scale_percent / 100)
height = int(img.shape[0] * scale_percent / 100)
dim = (width, height)
img = cv2.resize(img, dim, interpolation = cv2.INTER_AREA)

# Now we will sharpen the image using the kernel below.

kernel = np.array([[-1,-1,-1], 
                       [-1, 9,-1],
                       [-1,-1,-1]])

sharpened = cv2.filter2D(img, -1, kernel) 

# Invert the sharpened image
sharpened = np.invert(sharpened)

# Thresholding the inverted image to create a binary image
ret, thresh = cv2.threshold(sharpened, 100
                            , 255
                            , cv2.THRESH_BINARY) 
  
# The window showing output images with the corresponding thresholding techniques applied to the input images 
plt.imshow(thresh , cmap='Greys') 

# Save the puzzle image using Pillow Library
from PIL import Image  
img = Image.fromarray(np.uint8(thresh), 'L')
img.save('puzzle image 1'+'.png')
img.show()

# Create a text file in which we will save the nonogram of the thresholded binary image
with open('text puzzle 1.txt', 'w') as f:
    data_r = pd.DataFrame(columns=range(50),index=range(100))
    data_c = pd.DataFrame(columns=range(51,100),index=range(100))

    data = []

    col_no = 0
    for j in thresh:
        count = 1
        old = -1
        l = []
        for i in j:
            if i == old:
                count=count+1     
            else:
                if old == 0:
                    l.append(count)
                count = 1
            old = i

        if old == 0:
            l.append(count)

        try:
            if len(l) != 0:
                f.write(' '.join([str(i) for i in l]))
                f.write('\n')
        except:
            pass
        col_no = col_no+1


    f.write('\n')


    col_no = 51

    thresh = np.transpose(thresh)
    for j in thresh:
        count = 1
        old = -1
        l = []
        for i in j:
            if i == old:
                count=count+1     
            else:
                if old == 0:
                    l.append(count)
                count = 1
            old = i

        if old == 0:
            l.append(count)

        try:
            if len(l) != 0:
                f.write(' '.join([str(i) for i in l]))
                f.write('\n')
        except:
            pass
        col_no = col_no+1
    f.save()
    f.close()


# In[ ]:





# In[ ]:





# In[ ]:




