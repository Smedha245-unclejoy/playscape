from django.shortcuts import render,get_object_or_404
from posts.models import Post
from rest_framework import generics
from .serializers import PreferenceSerializer,CommentSerializer
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from .models import Preference

# Create your views here.

def postpreference(request, postid, userpreference):
    if request.method == 'POST':
        eachpost= get_object_or_404(Post, id=postid)
        obj=''
        valueobj=''
        try:
            obj = Preference.objects.get(user = request.user,post = eachpost)
            valueobj = obj.value #value of user preference
            valueobj = int(valueobj)
            userpreference = int(userpreference)
            if valueobj!=userpreference:
                obj.delete()
                upref = Preference()
                upref.user = request.user
                upref.post = eachpost
                if userpreference == 1 and valueobj!=1:
                    eachpost.likes +=1
                upref.save()
                eachpost.save()
                context= {'eachpost': eachpost,
                                  'postid': postid}
            elif valueobj == userpreference:
                obj.delete()

                if userpreference == 1:
                    eachpost.likes -= 1
                eachpost.save()
                context= {'eachpost': eachpost,
                                  'postid': postid}
        except Preference.DoesNotExist:
             upref = Preference()
             upref.user = request.user
             upref.post = eachpost
             upref.value = userpreference
             userpreference = int(userpreference)
             if userpreference == 1:
                 eachpost.likes+=1

             upref.save()
             eachpost.save()
             context= {'eachpost': eachpost,
                          'postid': postid}
    else:
        eachpost= get_object_or_404(Post, id=postid)
        context= {'eachpost': eachpost,
                          'postid': postid}

def createcomments(self,request,format='json'):
    if request.method == 'POST':
        queryset = User.objects.all()
        user = get_object_or_404(User,id=request.user.id)
        request.data['author_name'] = user.username
        post = Post.objects.filter(id = request.data['post_id'])
        data['post']=post
        serializer = CommentSerializer(post=post,author=request.user,text=data['text'])
        if serializer.is_valid():
            comment = serializer.save()
            if comment:
                json = serializer.data
                return Response(json, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class GetPreference(APIView):
    permissions=[IsAuthenticated]
    serializer_class = PreferenceSerializer
    def get(self,request,user_id,post_id):
        preference = Preference.objects.filter(post = post_id,user = user_id)
        if preference:
            value = preference.value
            return Response(value,status = status.HTTP_200_OK)
        return Response("no such post",status.HTTP_400_BAD_REQUEST)

class CommentsForPost(generics.ListAPIView):
    permissions = [IsAuthenticated]
    serializer_class = CommentSerializer

    def get_queryset(self,request,post_id):
        queryset = Comment.objects.filter(post=post_id)
        return queryset
