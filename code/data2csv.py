import sys
import pytesseract
from PIL import Image
import numpy as np
import matplotlib.pyplot as plt
import cv2
import platform
if(platform.system()=="Windows"):
    pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract'
else: 
    pytesseract.pytesseract.tesseract_cmd = r'usr/bin/tesseract'
    
# format of cords [((left,top),(right,botom))]
def cords2data(cords, baseimage):
    baseimage=baseimage
    data=[]
    for a,b in cords:
        cell=baseimage.crop((a[0],a[1],b[0],b[1]))
        data.append(pytesseract.image_to_string(cell, config='--psm 7'))


    return data

#take a string that indicate the file where we want to write
#the dataset(a datastructure of string)
#nbcol et nbline are the number of colum and the number of line
def data2csv(path,data,nbcol,nbline):
    with open(path, 'w') as f:
        for j in range(nbline):
            for i in range(nbcol):
                w=len(data[nbcol*j+i])
                if(platform.system()!="Windows"):
                    sub=data[nbcol*j+i][:w-2]
                else:
                    sub=data[nbcol*j+i][:w-1]
                w=len(sub) 
                if(w!=0):
                    if((sub[w-1]=='-')|(sub[w-1]=='.')|(sub[w-1]==',')):
                        sub=sub[:w-1]
                f.write(sub)
                if(i<nbcol-1):
                    f.write(';') 
            f.write("\n")
        
