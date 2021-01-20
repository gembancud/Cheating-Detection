# import necessary libs
import os
import uvicorn
import asyncio
import cv2
from starlette.routing import Route, WebSocketRoute
# from vidgear.gears.asyncio import WebGear
from CDApp.myWebgear import MyWebGear
from vidgear.gears import NetGear
from vidgear.gears.asyncio.helper import reducer
from starlette.responses import StreamingResponse
from starlette.config import Config
import sqlalchemy
import databases
import requests
import argparse

from CDApp.routes import hello_world, startGeneratePose, stopGeneratePose, startCheatDetection, stopCheatDetection, Echo
from CDApp.controller import Controller
from CheatDetection import CheatDetection
cd = CheatDetection()

config = Config('.env')
DATABASE_URL = config('DATABASE_URL')

metadata = sqlalchemy.MetaData()

report = sqlalchemy.Table(
    "reports",
    metadata,
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True),
    sqlalchemy.Column("confirmed", sqlalchemy.Boolean),
)

database = databases.Database(DATABASE_URL)

path = os.path.abspath(__file__)
dir_path = os.path.dirname(path)


options = {"frame_size_reduction": 40, "frame_jpeg_quality": 80,
           "frame_jpeg_optimize": True, "frame_jpeg_progressive": False,
           "custom_data_location": dir_path+"/CDApp/",
           }

# initialize WebGear app with same source
# also enable `logging` for debugging
web = MyWebGear(source='./sample.mp4', logging=True,
                database=database, **options)

FRAME_SKIP_CONSTANT = 3


async def my_frame_producer():
    frame_counter = 0

    while True:
        frame = Controller.server.recv()

        if frame is None:
            break

        # Do CheatDetection Here
        if Controller.generatePose:
            frame_counter += 1
            if frame_counter == FRAME_SKIP_CONSTANT:
                frame_counter = 0
                continue
            frame = cd.GeneratePose(frame)
        if Controller.generatePose and Controller.detectCheat:
            frame, cheating = cd.DetectCheat()
            if cheating:
                send_image(frame)

        # Do Live Updates
        # Controller.test.append("oten")

        # frame = reducer(frame, percentage=50)
        encodedImage = cv2.imencode('.jpg', frame)[1].tobytes()
        yield (b'--frame\r\nContent-Type:image/jpeg\r\n\r\n'+encodedImage+b'\r\n')
        await asyncio.sleep(0.01)


def send_image(frame, url="http://localhost:8000/api/core/snapshot/"):
    imencoded = cv2.imencode(".jpg", frame)[1]
    file = {'image': ('image.jpg', imencoded.tostring(),
                      'image/jpeg', {'Expires': '0'})}
    data = {'title': Controller.title, }
    try:
        response = requests.post(url, files=file, data=data, timeout=5)
        return response
    except:
        pass

# now create your own streaming response server


async def video_server(scope):
    Controller.enabled = True
    assert scope['type'] == 'http'
    # add your frame producer
    return StreamingResponse(my_frame_producer(), media_type='multipart/x-mixed-replace; boundary=frame')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Description of your program')
    parser.add_argument('-a', '--address',
                        help='address of server', default=None)
    args = parser.parse_args()

    # append new route to point your own streaming response server created above
    # new route for your frames producer will be `{address}/my_frames`
    web.routes.append(Route('/my_frames', video_server))
    web.routes.append(Route('/startGeneratePose', startGeneratePose))
    web.routes.append(Route('/stopGeneratePose', stopGeneratePose))
    web.routes.append(Route('/startCheatDetect', startCheatDetection))
    web.routes.append(Route('/stopCheatDetect', stopCheatDetection))
    web.routes.append(WebSocketRoute('/ws', Echo))

    Controller.server = NetGear(address=args.address, receive_mode=True, logging=True, pattern=2, **options)

    app = web()

    # run this app on Uvicorn server at address http://localhost:8000/
    uvicorn.run(app, host='localhost', port=8001)

    # close app safely
    web.shutdown()
