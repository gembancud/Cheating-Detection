# import required libraries
from vidgear.gears import NetGear, VideoGear
# from vidgear.gears import helper
import cv2
import argparse


def gstreamer_pipeline(
    capture_width=1280,
    capture_height=720,
    display_width=1280,
    display_height=720,
    framerate=60,
    flip_method=0,
):
    return (
        "nvarguscamerasrc ! "
        "video/x-raw(memory:NVMM), "
        "width=(int)%d, height=(int)%d, "
        "format=(string)NV12, framerate=(fraction)%d/1 ! "
        "nvvidconv flip-method=%d ! "
        "video/x-raw, width=(int)%d, height=(int)%d, format=(string)BGRx ! "
        "videoconvert ! "
        "video/x-raw, format=(string)BGR ! appsink"
        % (
            capture_width,
            capture_height,
            framerate,
            flip_method,
            display_width,
            display_height,
        )
    )


options = {'max_retries': 1000, }


def main():

    parser = argparse.ArgumentParser(description='Description of your program')
    parser.add_argument('-a', '--address',
                        help='address of server', default=None)
    parser.add_argument('-d', '--device',
                        help='desktop or nano', default='desktop')

    args = parser.parse_args()

    # define Netgear Client with `receive_mode = True` and default parameter
    client = NetGear(address=args.address, receive_mode=False,
                     pattern=2,  **options)

    # Run NanoVidGear Video
    # stream = VideoGear(source='./sample.mp4').start()

    # Run NanoVidgear PC Webcam
    if args.device == "desktop":
        stream = cv2.VideoCapture(0)

    elif args.device == "nano":
        stream = cv2.VideoCapture(gstreamer_pipeline(flip_method=0), cv2.CAP_GSTREAMER)

    # loop over
    while True:
        # receive frames from network
        (grabbed, frame) = stream.read()
        # check for received frame if Nonetype
        if frame is None:
            break
        # {do something with the frame here}
        # frame =helper.reducer(frame,50)
        client.send(frame)

    stream.stop()

    # safely close client
    client.close()


if __name__ == "__main__":
    main()
