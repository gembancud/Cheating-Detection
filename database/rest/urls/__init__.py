from django.urls import include, path
from rest_framework import routers
from .core import core_router


app_name = "rest"
urlpatterns = [
    path("core/", include(core_router.urls)),
]