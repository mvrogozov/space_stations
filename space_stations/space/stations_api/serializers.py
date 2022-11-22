from rest_framework.serializers import ModelSerializer

from stations.models import Command, Coordinates, Station


class StationSerializer(ModelSerializer):

    class Meta:
        model = Station
        fields = '__all__'
        read_only_fields = (
            'id',
            'create_date',
            'brake_date',
            'status'
        )

    def create(self, validated_data):
        station = Station.objects.create(**validated_data)
        Coordinates.objects.create(
            station=station
        )
        return station


class CommandSerializer(ModelSerializer):

    class Meta:
        model = Command
        fields = '__all__'


class CoordinatesSerializer(ModelSerializer):

    class Meta:
        model = Coordinates
        fields = (
            'x',
            'y',
            'z'
        )
