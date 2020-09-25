# import library
from vidgear.gears.asyncio import NetGear_Async
import cv2, asyncio

#initialize Server
client=NetGear_Async(logging=True, port=8001, pattern=2)

#Create a async frame generator as custom source
async def my_frame_generator():

        #Open any video stream such as live webcam video stream on first index(i.e. 0) device
        stream=cv2.VideoCapture(0) 

        # loop over stream until its terminated
        while True:

            # read frames
            (grabbed, frame)=stream.read()

            # check if frame empty
            if not grabbed:
                #if True break the infinite loop
                break

            # do something with the frame to be sent here

            # yield frame
            yield frame
            # sleep for sometime
            await asyncio.sleep(0.00001)


if __name__ == '__main__':
    #set event loop
    asyncio.set_event_loop(client.loop)
    #Add your custom source generator to client configuration
    client.config["generator"]=my_frame_generator() 
    #Launch the client 
    client.launch()
    try:
        #run your main function task until it is complete
        client.loop.run_until_complete(client.task)
    except (KeyboardInterrupt, SystemExit):
        #wait for interrupts
        pass
    finally:
        # finally close the client
        client.close()