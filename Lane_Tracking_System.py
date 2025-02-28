import cv2 as cv
import numpy as np

def rescaleFrame(frame, scale=1):

    width = int(frame.shape[1] * scale)
    height = int(frame.shape[0] * scale)
    
    dimensions = (width,height)
    
    return cv.resize(frame,dimensions, interpolation=cv.INTER_AREA)

# Define the region of interest to focus on lane detection
def region_of_interest(img):
    height = img.shape[0]
    width = img.shape[1]

    polygons = np.array([[(0,height),(width,height),(width//2,height//1.55)]],dtype=np.int32)

    mask=np.zeros_like(img)
    cv.fillPoly(mask,polygons,255)

    return cv.bitwise_and(img,img,mask=mask)

# Calculate the average center of detected lines
def average_line(lines):
    if len(lines) == 0:
        return None
    x_values = []
    y_values = []

    for x1,y1,x2,y2 in lines:
        x_values.extend([x1,x2])
        y_values.extend([y1,y2])

    if len(x_values)==0:
        return None

    x_mean = int(np.mean(x_values))
    y_mean = int(np.mean(y_values))

    return (x_mean, y_mean)    
    
video = cv.VideoCapture('Videos/vid3.mp4')

previous_direction = "Go straight"
previous_left_point = None
previous_right_point = None
previous_lane_center = None
turn_counter = 0
turn_thresholder = 0
direction = None

while True:
    ret, frame=video.read()
    if not ret:
        break

    rescale = rescaleFrame(frame,0.5)
    
    hsv = cv.cvtColor(rescale,cv.COLOR_BGR2HSV)

    minimum = np.array([0,0,200])
    maximum = np.array([180,50,255])
    
    mask = cv.inRange(hsv,minimum,maximum)

    gray = cv.cvtColor(rescale,cv.COLOR_BGR2GRAY)
    blur = cv.GaussianBlur(gray,(7,7),1)
    edge = cv.Canny(blur,50,150)
    roi = region_of_interest(edge)

    # Use Hought Transform to detect lines in the region of interest
    lines = cv.HoughLinesP(roi,1,np.pi/180,50,maxLineGap=60,minLineLength=50)
    if lines is not None:
        for line in lines:
            x1,y1,x2,y2 = line[0]
            cv.line(rescale,(x1,y1),(x2,y2),(0,255,0),3)
    
    left_lines = []
    right_lines = []
    
    if lines is not None:
        for line in lines:
            x1,y1,x2,y2 = line[0]
            slope = (y2-y1)/(x2-x1+ 0.00001)

            if slope < -0.3  :
                left_lines.append((x1,y1,x2,y2))
            elif slope > 0.3 :
                right_lines.append((x1,y1,x2,y2))
             
    left_point = average_line(left_lines)
    right_point = average_line(right_lines)  

    if left_point is None and previous_left_point is not None:
        left_point = previous_left_point
    if right_point is None and previous_right_point is not None:
        right_point = previous_right_point

    if left_point is not None:
        previous_left_point = left_point
    if right_point is not None:
        previous_right_point = right_point

    if previous_lane_center is None:
        previous_lane_center = rescale.shape[1]//2
     
     # Determine the direction based on the detected points
    if left_point is None or right_point is None:
        lane_center = previous_lane_center  
        direction = previous_direction
    elif left_point is None:       
        lane_center = right_point[0]  
        direction = "Turn right"
    elif right_point is None:      
        lane_center = left_point[0] 
        direction = "Turn left"
    else:
        lane_center = (left_point[0] + right_point[0])//2
        previous_lane_center = lane_center
        
    frame_center = rescale.shape[1] // 2
    
    lane_diff = lane_center - frame_center

    threshold = 16

    if  abs(lane_diff) < threshold:
        if turn_counter < turn_thresholder:
            turn_counter += 1
        else:
            direction = "Go straight"  
    else:
        turn_counter = 0
        if lane_diff > 0:
            direction = "Turn right"
        else:
            direction = "Turn left"
        
    if left_point is None or right_point is None:
        direction = previous_direction
    
    previous_direction = direction

    cv.putText(rescale,f'Direction = {direction}',(20,50),cv.FONT_HERSHEY_SIMPLEX,1,(0,255,0),2)
    
    cv.imshow('Lines',roi)
    cv.imshow('Video', rescale)
    
    if cv.waitKey(1)& 0xFF==ord("d"):
        break
        
video.release()
cv.destroyAllWindows()
