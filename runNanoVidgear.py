# import required libraries
from vidgear.gears import NetGear
import cv2


options = {'max_retries':1000, } 

#define Netgear Client with `receive_mode = True` and default parameter
client = NetGear( receive_mode = False, **options)

# open any valid video stream(for e.g `test.mp4` file)
# stream = VideoGear(source='./sample.mp4').start()
stream = cv2.VideoCapture(0)

# loop over
while True:
    # receive frames from network
    (grabbed, frame) = stream.read()
    # check for received frame if Nonetype
    if frame is None:
        break
    # {do something with the frame here}
    client.send(frame)

stream.stop()

# safely close client
client.close()