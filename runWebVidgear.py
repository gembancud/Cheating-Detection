# import necessary libs
import uvicorn, asyncio, cv2
from starlette.routing import Route
from vidgear.gears import NetGear
from vidgear.gears.asyncio import WebGear
from vidgear.gears.asyncio.helper import reducer
from starlette.responses import StreamingResponse
from CheatDetection import CheatDetection
cd = CheatDetection()


options={"frame_size_reduction": 40, "frame_jpeg_quality": 80, "frame_jpeg_optimize": True, "frame_jpeg_progressive": False}

# initialize WebGear app with same source
web = WebGear(source = './sample.mp4', logging = True, **options) # also enable `logging` for debugging 

async def my_frame_producer():
    server=NetGear(receive_mode=True, logging=True)
    
    while True:
        frame = server.recv()

        if frame is None:
            break

        # Do CheatDetection Here
        # frame = cd.GeneratePose(frame)
        # frame = cd.DetectCheat()

        # frame = reducer(frame, percentage=50)
        encodedImage = cv2.imencode('.jpg',frame)[1].tobytes()
        yield (b'--frame\r\nContent-Type:image/jpeg\r\n\r\n'+encodedImage+b'\r\n')
        await asyncio.sleep(0.01)

# now create your own streaming response server
async def video_server(scope):
  assert scope['type'] == 'http'
  return StreamingResponse(my_frame_producer(), media_type='multipart/x-mixed-replace; boundary=frame') # add your frame producer


if __name__ == '__main__':
    # append new route to point your own streaming response server created above
    web.routes.append(Route('/my_frames', endpoint=video_server)) #new route for your frames producer will be `{address}/my_frames`

    # run this app on Uvicorn server at address http://localhost:8000/
    uvicorn.run(web(), host='localhost', port=8000)

    # close app safely
    web.shutdown()


