from ..serializers.core import SnapshotSerializer
from rest_framework import viewsets

from core.models import Snapshot


class SnapshotViewSet(viewsets.ModelViewSet):
    queryset = Snapshot.objects.all()
    serializer_class = SnapshotSerializer