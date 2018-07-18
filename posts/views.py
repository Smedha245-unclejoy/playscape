from rest_framework.parsers import MultiPartParser
from rest_framework.permissions import IsAuthenticated
from posts.serializers import PostSerializer
from rest_framework.viewsets import ModelViewSet
from rest_framework import generics
from rest_framework.views import APIView
from posts.models import Post,PostImage
from rest_framework import status
from friends.models import Friendship
from django.db.models import Q
from rest_framework.decorators import parser_classes
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
# Create your views here.


@parser_classes((MultiPartParser,))
class Upload(ModelViewSet):
    """
    To create a new post including multiple images
    """
    permissions = [IsAuthenticated]
    parser_classes = MultiPartParser
    queryset = Post.objects.all()
    serializer_class = PostSerializer


    #def post(self,request,format=None):
    #    print("Inside create")
    #    self.parser_classes = (MultiPartParser,)
    #    queryset = Post.objects.all()
    #    serializer_class = PostSerializer
    #    serializer = PostSerializer(data = request.data)
    #    if serializer.is_valid():
    #        serializer.save()
    #        return Response(serializer.data)
class AllPosts(generics.ListAPIView):
    """
    To fetch all posts created by the user when he makes a request by himself using his user_id
    """
    permissions = [IsAuthenticated]
    serializer_class = PostSerializer
    def get_queryset(self):
        user_id = self.kwargs['user_id']
        queryset = Post.objects.filter(user_id=user_id,activity='active')
        return queryset

class PostDetail(APIView):
    """
    Detail view of a particular post created by the user
    """
    permissions = [IsAuthenticated]
    def get(self,request, post_id):
        """
        View individual post
        """
        id = self.kwargs['post_id']
        post = get_object_or_404(Post, pk=post_id)
         #pk is primary key for post table
        return Response(PostSerializer(post).data)

class PostFeed(generics.ListAPIView):
    """
    PostFeed first select * from posts where post.author=friend of user
    """
    permissions = [IsAuthenticated]
    serializer = PostSerializer
    def get_queryset(self):
        author = Friendship.objects.filter(Q(friend=self.request.user.id)|Q(creator=self.request.user.id))
        friend_id = author.friend.all()|author.creator.all()
        queryset = Post.objects.filter(activity='active',user_id=friend_id)
        return queryset
