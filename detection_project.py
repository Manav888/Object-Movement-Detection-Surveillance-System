# Import the required libraries
import AMP as amp
import numpy as np
import cv2
import time


# Set Window normal so we can resize it
cv2.namedWindow('frame', cv2.WINDOW_NORMAL)

# Note the starting time
start_time = time.time()

# Initialize these variables for calculating FPS
fps = 0
frame_counter = 0

# Read the video steram from the camera
cap = cv2.VideoCapture('http://192.168.254.11:8080/video') #without password
#cap = cv2.VideoCapture('http://samsung:samsung 456@192.168.254.11:8080/video')  #with password
# syantax ======  cv2.VideoCapture( protocol://username:password@host:port/video)

while (True):

    ret, frame = cap.read()
    if not ret:
        break

        # Calculate the Average FPS
    frame_counter += 1
    fps = (frame_counter / (time.time() - start_time))

    # Display the FPS
    cv2.putText(frame, 'FPS: {:.2f}'.format(fps), (20, 20), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 255), 1)

    # Show the Frame
    cv2.imshow('frame', frame)

    # Exit if q is pressed.
    if cv2.waitKey(1) == ord('q'):
        break
# Release Capture and destroy windows
cap.release()
cv2.destroyAllWindows()



# initlize video capture object
cap = cv2.VideoCapture('http://192.168.254.11:8080/video')

# you can set custom kernel size if you want
kernel = None

# initilize background subtractor object
foog = cv2.createBackgroundSubtractorMOG2(detectShadows=True, varThreshold=50, history=2800)

# Noise filter threshold
thresh = 1100

while (1):
    ret, frame = cap.read()
    if not ret:
        break

    # Apply background subtraction
    fgmask = foog.apply(frame)

    # Get rid of the shadows
    ret, fgmask = cv2.threshold(fgmask, 250, 255, cv2.THRESH_BINARY)

    # Apply some morphological operations to make sure you have a good mask
    # fgmask = cv2.erode(fgmask,kernel,iterations = 1)
    fgmask = cv2.dilate(fgmask, kernel, iterations=4)

    # Detect contours in the frame
    contours, hierarchy = cv2.findContours(fgmask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    if contours:

        # Get the maximum contour
        cnt = max(contours, key=cv2.contourArea)

        # make sure the contour area is somewhat hihger than some threshold to make sure its a person and not some noise.
        if cv2.contourArea(cnt) > thresh:
            # Draw a bounding box around the person and label it as person detected
            x, y, w, h = cv2.boundingRect(cnt)
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 0, 255), 2)
            cv2.putText(frame, 'Person Detected', (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.3, (0, 255, 0), 1,
                        cv2.LINE_AA)

    # Stack both frames and show the image
    fgmask_3 = cv2.cvtColor(fgmask, cv2.COLOR_GRAY2BGR)
    stacked = np.hstack((fgmask_3, frame))
    cv2.imshow('Combined', cv2.resize(stacked, None, fx=0.65, fy=0.65))

    k = cv2.waitKey(40) &amp; 0xff
    if k == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
