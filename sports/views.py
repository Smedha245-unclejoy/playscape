from django.shortcuts import render
from rest_framework import generics
from rest_framework.views import APIView
from sports.models import Sport,SportFollower
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework import generics
from rest_framework.decorators import parser_classes
from rest_framework.parsers import MultiPartParser
from rest_framework.permissions import IsAuthenticated
from sports.serializers import SportSerializer,SportFollowerSerializer

# Create your views here.


class SportView(APIView):
    permissions = [IsAuthenticated]
    def post(self, request, format='json'):
        serializer = SportSerializer(data=request.data)
        if serializer.is_valid():
            sport = serializer.save()
            if sport:
                json = serializer.data  #all user data
                return Response(json, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class SportsFollowedByUser(generics.ListAPIView):
    permissions = [IsAuthenticated]
    serializer_class = SportFollowerSerializer
    def get_queryset(self):
        user_id = self.request.user.id
        queryset = SportFollower.objects.filter(follower=user_id)
        return queryset
class SportFollowerView(APIView):
    permissions = [IsAuthenticated]
    def post(self, request, format='json'):
        request.data['follower']=self.request.user.id
        serializer = SportFollowerSerializer(data=request.data)
        if serializer.is_valid():
            sportFollow = serializer.save()
            if sportFollow:
                json = serializer.data
                return Response(json, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class AllSports(generics.ListAPIView):
    permissions = [IsAuthenticated]
    serializer_class = SportSerializer
    def get_queryset(self):
        queryset = Sport.objects.all()
        return queryset

@parser_classes((MultiPartParser,))
class SportUpdate(generics.UpdateAPIView):
    permissions = [IsAuthenticated]
    parser_classes = MultiPartParser
    queryset = Sport.objects.all()
    def post(self,request):
        instance=get_object_or_404(Sport,sport_name=request.data['sport_name'])
        if instance:
            serializer = SportSerializer(instance=instance,data=request.data)
            if serializer.is_valid():
                serializer.save(instance=instance,validated_data=serializer.validated_data)

                return Response(serializer.data)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
