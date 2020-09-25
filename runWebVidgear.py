# import necessary libs
import os
import uvicorn
import asyncio
import cv2
from starlette.routing import Route
# from vidgear.gears.asyncio import WebGear
from CDApp.myWebgear import MyWebGear
from vidgear.gears.asyncio.helper import reducer
from starlette.responses import StreamingResponse
from starlette.config import Config
import sqlalchemy
import databases

from CDApp.routes import hello_world, startGeneratePose, stopGeneratePose, startCheatDetection, stopCheatDetection
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
web = MyWebGear(source='./sample.mp4', logging=True, database= database, **options)


async def my_frame_producer():

    while True:
        frame = Controller.server.recv()

        if frame is None:
            break

        # Do CheatDetection Here
        if Controller.generatePose:
            frame = cd.GeneratePose(frame)
        if Controller.generatePose and Controller.detectCheat:
            frame = cd.DetectCheat()
            
        # frame = reducer(frame, percentage=50)
        encodedImage = cv2.imencode('.jpg', frame)[1].tobytes()
        yield (b'--frame\r\nContent-Type:image/jpeg\r\n\r\n'+encodedImage+b'\r\n')
        await asyncio.sleep(0.01)


# now create your own streaming response server
async def video_server(scope):
    Controller.enabled = True
    assert scope['type'] == 'http'
    # add your frame producer
    return StreamingResponse(my_frame_producer(), media_type='multipart/x-mixed-replace; boundary=frame')


if __name__ == '__main__':
    # append new route to point your own streaming response server created above
    # new route for your frames producer will be `{address}/my_frames`
    web.routes.append(Route('/my_frames', video_server))
    web.routes.append(Route('/startGeneratePose', startGeneratePose))
    web.routes.append(Route('/stopGeneratePose', stopGeneratePose))
    web.routes.append(Route('/startCheatDetect', startCheatDetection))
    web.routes.append(Route('/stopCheatDetect', stopCheatDetection))


    # run this app on Uvicorn server at address http://localhost:8000/
    uvicorn.run(web(), host='localhost', port=8000)

    # close app safely
    web.shutdown()
