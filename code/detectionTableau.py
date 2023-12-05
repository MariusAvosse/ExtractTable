import os
import cv2
import numpy as np
import matplotlib.pyplot as plt
import data2csv

def table(image_path):
    
    
    image=cv2.imread(image_path)

    gray_scale=cv2.cvtColor(image,cv2.COLOR_BGR2GRAY)#to transform the image to a greyscale image
    th1,img_bin = cv2.threshold(gray_scale,150,225,cv2.THRESH_BINARY)
    img_bin=~img_bin


    ### selecting min size as 15 pixels
    line_min_width = 15
    kernal_h = np.ones((1,line_min_width), np.uint8)
    kernal_v = np.ones((line_min_width,1), np.uint8)
    img_bin_h = cv2.morphologyEx(img_bin, cv2.MORPH_OPEN, kernal_h)
    img_bin_v = cv2.morphologyEx(img_bin, cv2.MORPH_OPEN, kernal_v)
    img_bin_final=img_bin_h|img_bin_v #end where the table is detected

    _, labels, stats,_ = cv2.connectedComponentsWithStats(~img_bin_final, connectivity=8, ltype=cv2.CV_32S)
    bounding=[]
    for x,y,w,h,area in stats[2:]:
        top=y
        left=x
        bottom=y+h
        right=x+w
        
        bounding.append(((left,top),(right,bottom)))
        cv2.rectangle(image,(x,y),(x+w,y+h),(0,255,0),2)
    return bounding

def cleaningline(cords,baseimage):
    last=(cords[0][0],cords[0][1])
    empty=True
    i=0
    for a,b in cords:
        if(a[1]>=last[1][1]):
            if(empty):
                return cords[i:]
            else:
                return cords
        last=(a,b)
        i+=1
        cell=baseimage.crop((a[0],a[1],b[0],b[1]))
        if np.mean(cell) < 254:
                if(cell.size[0]>1): #need some fine tuning but its for really little cell detected which fools the mean because of the size
                    empty=False
    return cords

def cleaninglastline(cords,baseimage):
    last=(cords[0][0],cords[0][1])
    empty=True
    i=0
    truei=0
    for a,b in cords:
        if(a[1]>=last[1][1]): 
            empty=True
            truei=i
        last=(a,b)
        i+=1
        cell=baseimage.crop((a[0],a[1],b[0],b[1]))
        if np.mean(cell) < 254:
                if(cell.size[0]>1): #need some fine tuning but its for really little cell detected which fools the mean because of the size
                    empty=False
    if(empty):
        return cords[:truei]
    else:
        return cords

def cleaningcol(cords,baseimage):

    cordssave=cords
    last=((cords[0][0],cords[0][1]))
    emptygauche=True
    a,b=cords[0]
    cell=baseimage.crop((a[0],a[1],b[0],b[1]))
    if np.mean(cell) < 254:
        if(cell.size[0]>1): #need some fine tuning but its for really little cell detected which fools the mean because of the size
            emptygauche=False
    emptydroite=True
    i=0
    for a,b in cords:
        if(a[1]>=last[1][1]):
            cell=baseimage.crop((a[0],a[1],b[0],b[1]))
            if np.mean(cell) < 254:
                if(cell.size[0]>1): #need some fine tuning but its for really little cell detected which fools the mean because of the size
                    emptygauche=False
            cell=baseimage.crop((last[0][0],last[0][1],last[1][0],last[1][1]))
            if np.mean(cell) < 254:
                if(cell.size[0]>1): #need some fine tuning but its for really little cell detected which fools the mean because of the size
                    emptydroite=False
        last=(a,b)
        i+=1
    cell=baseimage.crop((a[0],a[1],b[0],b[1]))
    if np.mean(cell) < 254:
        if(cell.size[0]>1): #need some fine tuning but its for really little cell detected which fools the mean because of the size
            emptydroite=False
    cords=cordssave
    cordsret=[]
    last=(cords[0][0],cords[0][1])
    for a,b in cords:
        if(a[1]>=last[1][1]):
            if(emptydroite):
                cordsret=cordsret[:-1]
            if(not emptygauche):
                cordsret.append((a,b))
        else:
            cordsret.append((a,b))
        last=(a,b)
    if(emptydroite):
        cordsret=cordsret[:-1]
    if(emptygauche):
        cordsret=cordsret[1:]
    return cordsret
def cleaning(cords,baseimage): 
    cords=cleaninglastline(cords,baseimage)
    cords=cleaningcol(cords,baseimage)
    cords=cleaningline(cords,baseimage)
    return cords
    cords2=[]
    i=0   
    for i in range(len(cords)):
        a,b=cords[i]
        cell=baseimage.crop((a[0],a[1],b[0],b[1]))
        if np.mean(cell) < 254:
                if(cell.size[0]>1): #need some fine tuning but its for really little cell detected which fools the mean because of the size
                    cords2.append((a,b))
    return cords2
    """
    WIP
    lasta,lastb=cords[0]
    validlast=False
    cords2=[]
    i=0
    t=False
    validc=0
    cc=0
    first=True
    for i in range(len(cords)-1):
        a,b=cords[i]
        c,d=cords[i+1]
        cell=baseimage.crop((a[0],a[1],b[0],b[1]))
        
        if(a[1]>=lastb[1]):
            first=False
            cc=0
            
        if np.mean(cell) < 254:
                if(cell.size[0]>1): #need some fine tuning but its for really little cell detected which fools the mean because of the size
                    cords2.append((a,b))
                    t=True
                    cc+=1

        else:
            if(first):
                if (validlast) and (not (c[1]>=b[1])) and (not (a[1]>=lastb[1]) ):
                    cords2.append((a,b))
                    t=True
                    cc+=1
            else:
                if (validlast) and (cc<=validc):
                    cords2.append((a,b))
                    t=True
                    cc+=1

        if(t):
            validlast=True
            if(first):
                validc+=1
        else:
            validlast=False
        t=False
        lasta,lastb=a,b
        
    a,b=cords[i+1]
    cell=baseimage.crop((a[0],a[1],b[0],b[1]))
    if np.mean(cell) < 254:
        if(cell.size[0]>1): #need some fine tuning but its for really little cell detected which fool the mean because of the size
            cords2.append((a,b))
            t=True
    else:
            if (validlast) and (not (c[1]>=b[1])) and (not (a[1]>=lastb[1]) ):
                cords2.append((a,b))
                t=True
                    
    return cords2
    """

def col(cords):
    last=cords[0]
    nbcol=0
    for a,b in cords:
            if(a[1]>=last[1][1]):
                return nbcol
            nbcol+=1
            last=(a,b)
    return nbcol 

def line(cords):
    last=cords[0]
    nbline=1
    for a,b in cords:
        if(a[1]>=last[1][1]):
                nbline+=1
        last=(a,b)

    return nbline 
    

