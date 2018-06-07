from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import generics
from rest_framework.parsers import JSONParser
from django.contrib.auth import authenticate
from rest_framework import status,viewsets,views
from sportsapp.serializers import UserSerializer,LoginSerializer,PasswordResetSerializer,ProfileSerializer
from django.contrib.gis.geos import Point
from django.shortcuts import get_object_or_404
from django.db.models import F
from django.contrib.gis.measure import Distance
from rest_framework.pagination import LimitOffsetPagination
#from rest_framework.authtoken.models import Token
from sportsapp.permissions import IsAuthenticatedOrCreate
from rest_framework.permissions import AllowAny
from django.contrib.auth.models import User
from .models import Profile
from oauth2_provider.models import Application
from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import make_password
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
# Create your views here.
class UserCreate(APIView):
    """
    Creates the user.
    """
    permission_classes = (IsAuthenticatedOrCreate,)
    serializer_class = UserSerializer
    def post(self, request, format='json'):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            if user:
                #token = Token.objects.create(user=user)#creates token
                json = serializer.data  #all user data
                #json['token'] = token.key  #all adding token in the to be returned json data
                #json['client_id'] = application_object.client_id
                #json['client_secret'] = application_object.client_secret
                return Response(json, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ForgotPassword(APIView):
    """
    Sends an email to the user to reset Password
    """
    permission_classes=(IsAuthenticatedOrCreate,)
    def post(self,request,format='json',*args,**kwargs):
        serializer = PasswordResetSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        PasswordResetSerializer.reset_password(request,serializer.data['email'])
        return Response({'status': 'password reset'})


class Login(APIView):
    """
    Verifying the users using username and password and generating the access_token
    """
    permission_classes=(IsAuthenticatedOrCreate,)
    #User = get_user_model()
    #queryset = User.objects.all()
    #serializer_class = LoginSerializer

    #def get_queryset(self):
        #queryset = super(Login, self).get_queryset()
        #return queryset.filter(pk=self.request.user.pk)
    parser_classes = ((JSONParser,))
    def post(self, request, format='json'):
        User = get_user_model()
        serializer_class = LoginSerializer
        data = request.data
        username = data['username']
        password_raw = data['password']
        password = make_password(password_raw,salt=None,hasher='default')
        user = authenticate(username=username,password=password_raw)
        if user is not None:
            #json=LoginSerializer.get_access_token(user)
            return Response(LoginSerializer.get_access_token(user),status=status.HTTP_200_OK)
        else :
            return Response(status=status.HTTP_422_UNPROCESSABLE_ENTITY)

# version GEO FIRST with pagination
#@api_view(['GET', ]
class NearbyUserList(viewsets.ViewSet):

    @staticmethod
    def list(request, username, current_latitude, current_longitude) -> Response:
        paginator = LimitOffsetPagination()
        paginator.max_limit = 250
        paginator.default_limit = 20
        user = get_object_or_404(User, username=username)
        user_location = Point(float(current_longitude), float(current_latitude))
        users = paginator.paginate_queryset(Users.objects.filter(
            last_location__distance_lte=(
            user_location,
            Distance(km=min(user.prefered_radius, F('prefered_radius'))))
           ).distance(user_location).order_by('distance'))

        return Response(
            data={'entries': [x.to_dict() for x in users], 'limit': paginator.limit,
                  'offset': paginator.offset, 'overall_count': paginator.count},
            status=status.HTTP_200_OK)

class AuthInfoUpdateView(generics.UpdateAPIView):
    permission_classes = (IsAuthenticatedOrCreate,)
    serializer_class = UserSerializer
    queryset = User.objects.all()
    lookup_field = 'pk'

    def patch(self, request, *args, **kwargs):
        instance=get_object_or_404(User,email=request.data['email'])
        serializer = UserSerializer(instance=instance,data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class SelfCreateProfile(APIView):
    permission_classes = (IsAuthenticatedOrCreate,)
    serializer_class = ProfileSerializer
    def post(self, request, format='json'):
        request.data['user']=request.user.id
        serializer = ProfileSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class GetUser(APIView):
    permission_classes = (IsAuthenticatedOrCreate,)
    def get(self,request):
        user = get_object_or_404(User,pk=request.user.id)
        if user:
            return Response(UserSerializer(user).data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
