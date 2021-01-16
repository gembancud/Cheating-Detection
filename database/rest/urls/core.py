from rest_framework import routers

from ..views.core import SnapshotViewSet


core_router = routers.DefaultRouter()
core_router.register(r"snapshot", SnapshotViewSet)