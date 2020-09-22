from starlette.templating import Jinja2Templates
from starlette.routing import Route
from starlette.responses import RedirectResponse


from CDApp.controller import Controller

import os
path = os.path.abspath(__file__)
dir_path = os.path.dirname(path)

template=Jinja2Templates(directory=dir_path+'/templates')

async def hello_world(request):
    Controller.isfocused = False
    page="hello.html"
    context={"request": request}
    return template.TemplateResponse(page, context)

async def startGeneratePose(request):
    Controller.generatePose = True
    return RedirectResponse(url='/')

async def stopGeneratePose(request):
    Controller.generatePose = False
    return RedirectResponse(url='/')

async def startCheatDetection(request):
    Controller.detectCheat = True
    return RedirectResponse(url='/')

async def stopCheatDetection(request):
    Controller.detectCheat = False
    return RedirectResponse(url='/')
