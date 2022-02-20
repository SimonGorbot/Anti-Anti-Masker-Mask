from imutils.video import VideoStream
from imutils.video import FPS
import face_recognition
import imutils
import pickle
import time
import cv2
import serial

# Initialize 'currentname' to trigger only when a new person is identified.
currentname = "unknown"
# Determine faces from encodings.pickle file model created from train_model.py
encodingsP = "encodings.pickle"

# load the known faces and embeddings along with OpenCV's Haar
# cascade for face detection
print("[INFO] loading encodings + face detector...")
# data = pickle.loads(open(encodingsP, "rb").read())

# initialize the video stream and allow the camera sensor to warm up
# Set the ser to the followng
# src = 0 : for the build in single web cam, could be your laptop webcam
# src = 2 : I had to set it to 2 inorder to use the USB webcam attached to my laptop
# vs = VideoStream(src=2,framerate=10).start()
# vs = VideoStream(usePiCamera=True).start()
cam = cv2.VideoCapture("http://192.168.137.206:8080/video")
time.sleep(2.0)

serialPort = serial.Serial(port="COM4", baudrate=115200, bytesize=8)

# loop over frames from the video file stream
while True:
    # grab the frame from the threaded video stream and resize it
    # to 500px (to speedup processing)
    ret, frame = cam.read()

    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    # frame = cv2.resize(frame, s
    frame = imutils.resize(frame, width=500)
    # Detect the fce boxes
    boxes = face_recognition.face_locations(frame)

    for (top, right, bottom, left) in boxes:
        # draw the predicted face name on the image - color is in BGR
        cv2.rectangle(frame, (left, top), (right, bottom),
                      (0, 255, 225), 2)
    # compute the facial embeddings for each face bounding box
    # encodings = face_recognition.face_encodings(frame, boxes)
    # names = []

    # display the image to our screen
    cv2.imshow("Facial Recognition is Running", frame)
    key = cv2.waitKey(1) & 0xFF

    # quit when 'q' key is pressed
    if key == ord("q"):
        break

    if len(boxes) != 0:
        num = 1
        serialPort.write(num) #if maskless face detected, then send 1 to arduino
        time.sleep(2.00)
# update the FPS counter
# stop the timer and display FPS information
print("[INFO] elasped time: {:.2f}".format(fps.elapsed()))
print("[INFO] approx. FPS: {:.2f}".format(fps.fps()))

# do a bit of cleanup
cv2.destroyAllWindows()
cam.stop()