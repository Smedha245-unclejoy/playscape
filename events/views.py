from django.shortcuts import render
from rest_framework.views import APIView
from .serializers import EventSerializer,PartcipatorsSerializer
from .models import Event,Participators
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from rest_framework import generics

# Create your views here.

class CreateEventView(APIView):
    permissions = [IsAuthenticated]
    def post(self,request,format='json'):
        serializer = EventSerializer

        all_events = Event.objects.filter(date = request.data['date'],playground_destination=request.data['playground_destination'])
        if all_events:
            for events in all_events:
                if request.data['time_from'] > events.time_from:
                     if request.data['time_from'] >= events.time_from + events.duration:
                            if serializer.is_valid():
                                event = serializer.save()
                                if event:
                                    json = serializer.data
                                    return Response(json,status=status.HTTP_201_CREATED)

                            return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
                     json = 'The timing of this event collides with an event already created'
                     return Response(json,status=status.HTTP_409_CONFLICT)
                json = 'The timing of this event collides with an event already created'
                return Response(json,status=status.HTTP_409_CONFLICT)

                if request.data['time_from'] < events.time_from:
                      if request.data['time_to'] <= events.time_from:
                            if serializer.is_valid():
                                event = serializer.save()
                                if event:
                                    json = serializer.data
                                    return Response(json,status=status.HTTP_201_CREATED)

                            return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
                      json = 'The timing of this event collides with an event already created'
                      return Response(json,status=status.HTTP_409_CONFLICT)
                json = 'The timing of this event collides with an event already created'
                return Response(json,status=status.HTTP_409_CONFLICT)

                if request.data['time_from'] == events.time_from:
                      json = 'The timing of this event collides with an event already created'
                      return Response(json,status=status.HTTP_409_CONFLICT)

        if serializer.is_valid():
            event = serializer.save()
            if event:
                json = serializer.data
                return Response(json,status=status.HTTP_201_CREATED)

        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)


class UpdateParticipatorStatus(generics.UpdateAPIView):
    permissions = [IsAuthenticated]
    serializer_class = PartcipatorsSerializer
    queryset = Participators.objects.all()
    lookup_field = 'participant_name'

    def post(self,request, *args, **kwargs):
        instance = get_object_or_404(Participators,participant_name=request.data['participant_name'],event=request.data['event'])
        if instance:
            serializer = PartcipatorsSerializer(instance=instance,data=request.data)
            if serializer.is_valid():
                serializer.save(instance=instance,validated_data=serializer.validated_data)

                return Response(serializer.data)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
