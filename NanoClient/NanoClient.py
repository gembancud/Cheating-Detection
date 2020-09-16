from NanoClient.CVClient import CVClient
import cv2

def nanoClient(camera, server_addr, stream_fps):
    streamer= None
    try:
        streamer = CVClient(server_addr, stream_fps).setup() 
        camera = cv2.VideoCapture(camera)
        if not camera.isOpened():
            raise RuntimeError('Could not start camera.')

        while True:
            _, img = camera.read()
            # cv2.imshow("NanoClient", img)
            # if cv2.waitKey(1) & 0xFF == ord("q"):
            #     break
            streamer.send_data(img)
            # if streamer.check_exit():
            #     break

    finally:
        if streamer is not None:
            streamer.close()
        print("Program Ending")