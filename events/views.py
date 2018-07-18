from django.shortcuts import render
from rest_framework.views import APIView
from .serializers import EventSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from rest_framework import generics

# Create your views here.

class CreateEventView(APIView):
    permissions = [IsAuthenticated]
    def post(self,request,format='json'):
        serializer = EventSerializer
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
