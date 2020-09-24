from vidgear.gears import NetGear

options = {'max_retries':1000, } 

class Controller:
    enabled = False
    isfocused = False
    server = NetGear(receive_mode=True, logging=True, **options)
    generatePose = False
    detectCheat = False

