# import required libraries
from vidgear.gears import NetGear, VideoGear
# from vidgear.gears import helper
import cv2
import argparse
import time


def gstreamer_pipeline(
    capture_width=640,
    capture_height=480,
    display_width=640,
    display_height=480,
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


options = {
    "max_retries": 1000,
    "bidirectional_mode": True,
    "compression_format": ".jpg",
    "compression_param": (
        cv2.IMREAD_COLOR,
        [
            cv2.IMWRITE_JPEG_QUALITY,
            70,
            cv2.IMWRITE_JPEG_PROGRESSIVE,
            True,
            cv2.IMWRITE_JPEG_OPTIMIZE,
            True,
        ],
    ),
}


def main():

    parser = argparse.ArgumentParser(description='Description of your program')
    parser.add_argument('-a', '--address',
                        help='address of server', default=None)
    parser.add_argument('-d', '--device',
                        help='desktop or nano', default='desktop')
    parser.add_argument('-s', '--source',
                        help='path to video', default=None)

    args = parser.parse_args()

    # define Netgear Client with `receive_mode = True` and default parameter
    client = NetGear(address=args.address, receive_mode=False,
                     pattern=1,  **options)

    # Run NanoVidGear Video
    # stream = VideoGear(source='./sample.mp4').start()

    # Run NanoVidgear PC Webcam
    if args.device == "desktop":
        if args.source:
            stream = cv2.VideoCapture(args.source)
        else:
            stream = cv2.VideoCapture(0)

    elif args.device == "nano":
        stream = cv2.VideoCapture(gstreamer_pipeline(
            flip_method=0), cv2.CAP_GSTREAMER)

    # loop over
    if args.source:
        frame_counter = 0
        fps = stream.get(cv2.CAP_PROP_FPS)
        print(f"Fps is {fps}")
        while True:
            # receive frames from network
            (grabbed, frame) = stream.read()
            # check for received fram e if Nonetype
            if frame is None:
                break

            # time.sleep(1/(1.82*fps))

            frame_counter += 1
            if frame_counter == stream.get(cv2.CAP_PROP_FRAME_COUNT):
                frame_counter=0
                stream.set(cv2.CAP_PROP_POS_FRAMES,0)
            # {do something with the frame here}
            # frame =helper.reducer(frame,50)
            client.send(frame)

    else:
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
