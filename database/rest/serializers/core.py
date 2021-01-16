from rest_framework import serializers

from core.models import Snapshot


class SnapshotSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Snapshot
        fields = ["title", "image",]