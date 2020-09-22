from vidgear.gears import NetGear

class Controller:
    enabled = False
    isfocused = False
    server = NetGear(receive_mode=True, logging=True)
    generatePose = False
    detectCheat = False

