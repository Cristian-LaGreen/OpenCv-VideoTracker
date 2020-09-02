#libraries I use for this thing
import cv2
import numpy as np
from matplotlib import pyplot as plt
#Calling the tracker and video for capture
cap=cv2.VideoCapture('Resources/bouncing_cart.mov')
#tracker = cv2.TrackerMOSSE_create()
tracker=cv2.TrackerCSRT_create()
succes,img=cap.read()
bbox=cv2.selectROI('Tracking',img,False)
tracker.init(img,bbox)

yvector = []
xvector = []
tvector=[]
#Function that keeps drawing the box arround the object

def drawBox(img,bbox):
    x,y,w,h=int(bbox[0]),int(bbox[1]),int(bbox[2]),int(bbox[3])
    cv2.rectangle(img,(x,y),(x+w,y+h),(0,255,0),2)

frames=0
#infinity Loop
while True:

    timer=cv2.getTickCount()
    succes1,img=cap.read()
    succes,bbox=tracker.update(img)


    #the way to collect position data of the object
    x, y = int(bbox[0]), int(bbox[1])
    xvector.append(x)
    yvector.append(y)
    tvector.append(frames)
    frames=frames+1

    #Tells if it stills Tracking and displays it on the screen
    if succes == True:
        drawBox(img,bbox)
        cv2.putText(img, 'Tracking', (75, 75), cv2.FAST_FEATURE_DETECTOR_TYPE_7_12, 1, (255, 0, 0), 1)
    else:
        cv2.putText(img,'Lost', (75, 75), cv2.FAST_FEATURE_DETECTOR_TYPE_7_12, 1, (0, 0, 255), 1)


    fps=cv2.getTickFrequency()/(cv2.getTickCount()-timer)
    cv2.putText(img,str(int(fps)),(75,50),cv2.FAST_FEATURE_DETECTOR_TYPE_7_12,1,(0,0,255),1)

    #Tells if the video end and if the frame size is null.

    if succes1:
        height, width, channels = img.shape
        if height>0 and width>0:
            cv2.imshow('Tracking',img)
    else:
        break
    if cv2.waitKey(1) & 0xFF==ord('q'):
        break

#Time vector
mseconds=[]
for i in tvector:
    mseconds.append(tvector[i]*int(fps))

#repositioning the of reference

yposition=list()
xposition=list()
for h in yvector:
    if h - height >= 0:
        yposition.append(h-height)
    else:
        yposition.append((h-height)*-1)
for w in xvector:
    width=0
    if w - width >= 0:
        xposition.append(w-width)
    else:
        xposition.append((w-width)*-1)

#first derivate for the velocity vector

n = len(tvector)
dx = ((tvector[-1] - tvector[0]) / n - 1)  #  Delta
ypx = np.zeros_like(tvector)  #vector full of zeros
for i in range(n):
    if i == 0:
        ypx[i] = (xvector[i + 1] - xvector[i]) / dx
    elif i == n - 1:
        ypx[i] = (xvector[i] - xvector[i - 1]) / dx
    else:
        ypx[i] = (xvector[i + 1] - xvector[i - 1]) / (2 * dx)

ypy = np.zeros_like(tvector)  # zeros vector
for i in range(n):
    if i == 0:
        ypy[i] = (yvector[i + 1] - yvector[i]) / dx
    elif i == n - 1:
        ypy[i] = (yvector[i] - yvector[i - 1]) / dx
    else:
        ypy[i] = (yvector[i + 1] - yvector[i - 1]) / (2 * dx)

#Second derivate

n=len(tvector)
dx=((tvector[-1]-tvector[0])/n-1)

yppx=np.zeros_like(tvector)

for i in range(n):
    if i==0:
        yppx[i]=(xvector[i+2]-2*xvector[i+1]+xvector[i])/(dx**2)
    elif i==n-1:
        yppx[i]=(xvector[i]-2*xvector[i-1]+xvector[i-2])/(dx**2)
    else:
        yppx[i]=(xvector[i+1]-2*xvector[i]+xvector[i-1])/(dx**2)

yppy=np.zeros_like(mseconds)

for i in range(n):
    if i==0:
        yppy[i]=(yvector[i+2]-2*yvector[i+1]+yvector[i])/(dx**2)
    elif i==n-1:
        yppy[i]=(yvector[i]-2*yvector[i-1]+yvector[i-2])/(dx**2)
    else:
        yppy[i]=(yvector[i+1]-2*yvector[i]+yvector[i-1])/(dx**2)


#Position X and Y
plt.plot(xvector,yvector)
plt.xlabel('Posicion x[Pixeles]')
plt.ylabel('Posicion y[Pixeles]')
plt.title('Movimiento del sistema')
plt.grid(True)
plt.show()

#Position over time
plt.plot(tvector,xvector, label="Posicion X")
plt.plot(tvector,yvector, label='Posicion Y')
plt.xlabel('Tiempo [Frames]')
plt.ylabel('Posicion[Pixeles]')
plt.title('Grafica de Posicion')
plt.legend()
plt.grid(True)
plt.show()

#Velocity over time

plt.plot(tvector,ypx,label="Velocidad X")
plt.plot(tvector,ypy,label="Velocidad Y")
plt.xlabel('Tiempo[Frames]')
plt.ylabel('Velocidad[Pixeles/Frames]')
plt.title('Grafica de Velocidad')
plt.legend()
plt.grid(True)
plt.show()

#Aceletations over time
plt.plot(tvector,yppx,label="Aceleracion X")
plt.plot(tvector,yppy,label="Aceleracion Y")
plt.xlabel('Tiempo[Frames]')
plt.ylabel('Aceleracion[Pixeles/Frames^2]')
plt.title('Grafica de Aceleracion')
plt.legend()
plt.grid(True)
plt.show()