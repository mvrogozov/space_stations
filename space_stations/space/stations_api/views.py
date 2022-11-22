from django.shortcuts import get_object_or_404
from django.utils import timezone
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from stations.models import Station

from .serializers import (CommandSerializer, CoordinatesSerializer,
                          StationSerializer)


class StationViewSet(ModelViewSet):
    model = Station
    serializer_class = StationSerializer
    queryset = Station.objects.all()

    @action(
        detail=True,
        methods=['get', 'post']
    )
    def state(self, request, pk):
        obj = get_object_or_404(self.model.objects.select_related(), id=pk)
        if request.method == 'GET':
            serializer = CoordinatesSerializer(instance=obj.coordinates)
            return Response(serializer.data, status=status.HTTP_200_OK)
        serializer = CommandSerializer(data=request.data)
        serializer.initial_data['station'] = pk
        serializer.is_valid(raise_exception=True)
        axis = serializer.validated_data.get('axis')
        distance = serializer.validated_data.get('distance')
        serializer.save()
        x = y = z = 0
        if axis == 'x':
            x = obj.coordinates.x + distance
            obj.coordinates.x = x
        if axis == 'y':
            y = obj.coordinates.y + distance
            obj.coordinates.y = y
        if axis == 'z':
            z = obj.coordinates.z + distance
            obj.coordinates.z = z
        if (x < 0) or (y < 0) or (z < 0):
            obj.status = 'BR'
            obj.brake_date = timezone.now()
        obj.coordinates.save()
        obj.save()
        serializer = CoordinatesSerializer(instance=obj.coordinates)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
