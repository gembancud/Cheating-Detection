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
import aiohttp
import argparse
import numpy as np

from CDApp.routes import startGeneratePose, stopGeneratePose, startCheatDetection, stopCheatDetection, Echo, startAll, stopAll
from CDApp.controller import Controller
from CheatDetection import CheatDetection
cd = CheatDetection()

path = os.path.abspath(__file__)
dir_path = os.path.dirname(path)


options = {"frame_size_reduction": 50, "frame_jpeg_quality": 80,
           "frame_jpeg_optimize": True, "frame_jpeg_progressive": False,
           "custom_data_location": dir_path+"/CDApp/",
           }

# initialize WebGear app with same source
# also enable `logging` for debugging
web = MyWebGear(logging=True, **options)

FRAME_SKIP_CONSTANT = 3  # Higher Number More Skips
URL = "http://localhost:8000/api/core/snapshot/"

session = aiohttp.ClientSession()


async def my_frame_producer():
    frame_counter = 0

    session = aiohttp.ClientSession()

    while True:
        frame = Controller.server.recv()
        if frame is None:
            break
        frame = await reducer(frame[1], percentage=25)

        # Do CheatDetection Here
        cheating = False
        if Controller.generatePose and not Controller.detectCheat:
            Skip, frame_counter = frame_skip(
                frame_counter, FRAME_SKIP_CONSTANT)
            if Skip:
                continue
            frame = cd.GeneratePose(frame)
        elif not Controller.generatePose and Controller.detectCheat:
            Skip, frame_counter = frame_skip(
                frame_counter, FRAME_SKIP_CONSTANT+1)
            if Skip:
                continue
            frame = cd.GeneratePose(frame)
            frame, cheating = cd.DetectCheat(ShowPose=False)
        elif Controller.generatePose and Controller.detectCheat:
            Skip, frame_counter = frame_skip(
                frame_counter, FRAME_SKIP_CONSTANT+1)
            if Skip:
                continue
            frame = cd.GeneratePose(frame)
            frame, cheating = cd.DetectCheat(ShowPose=True)

        # Do Live Updates
        if cheating:
            imencoded = cv2.imencode(".jpg", frame)[1]
            form = aiohttp.FormData()
            form.add_field('title', Controller.title)
            form.add_field('image',
                      imencoded.tostring(),
                      filename=f'{Controller.title}.jpg',
                      content_type='image/jpeg')
            async with session.post(URL, data=form) as response:
                print(await response.read())

        frame = cv2.resize(frame, (640, 480))
        encodedImage = cv2.imencode('.jpg', frame)[1].tobytes()
        yield (b'--frame\r\nContent-Type:image/jpeg\r\n\r\n'+encodedImage+b'\r\n')
        await asyncio.sleep(0.01)

    await session.close()


def frame_skip(frame_counter, constant):
    frame_counter += 1
    if frame_counter != constant:
        return True, frame_counter
    else:
        return False, 0


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
    web.routes.append(Route('/startAll', startAll))
    web.routes.append(Route('/stopAll', stopAll))
    web.routes.append(WebSocketRoute('/ws', Echo))

    netgear_options = {
        "max_retries": 1000,
        "bidirectional_mode": True,
        "compression_format": ".jpg",
        "compression_param": (
            cv2.IMREAD_COLOR,
            [
                cv2.IMWRITE_JPEG_QUALITY,
                60,
                cv2.IMWRITE_JPEG_PROGRESSIVE,
                False,
                cv2.IMWRITE_JPEG_OPTIMIZE,
                True,
            ],
        ),
    }

    Controller.server = NetGear(
        address=args.address, receive_mode=True, logging=True, pattern=1, **netgear_options)

    app = web()

    # run this app on Uvicorn server at address http://localhost:8001/
    uvicorn.run(app, host='0.0.0.0', port=8001)

    session.close()

    # close app safely
    web.shutdown()
