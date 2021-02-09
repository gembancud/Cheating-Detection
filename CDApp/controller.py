from collections import deque

options = {'max_retries': 1000, }


class Controller:
    enabled = False
    isfocused = False
    server = None
    generatePose = False
    detectCheat = False
    test = deque()
    title = "default-title"
    producer = None
