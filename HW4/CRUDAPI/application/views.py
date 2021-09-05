from django.http.response import HttpResponse
from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.serializers import Serializer
from .models import *
from .serializers import *
from rest_framework.views import APIView
from rest_framework import generics

# Create your views here.

class ListPostAPIView(APIView):
    def get(self , request , username):
        if not Post.objects.filter(username=username).exists():
            return HttpResponse('Does not exist')
        posts = Post.objects.filter(username = username).order_by('-date_created')
        serializer = PostSerializer(posts , many=True)
        return Response(serializer.data)

class PostDetailAPIView(APIView):
    def get(self , request, pk):
        post = Post.objects.get(post_id=pk)
        serializer = PostSerializer(post, many=False)
        return Response(serializer.data)

class CreatePostAPIView(APIView):
    def post(self , request):
        serializer = PostSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors)

class UpdatePostAPIView(APIView):
    def put(self , request , pk):
        data = request.data
        if not Post.objects.filter(post_id=pk).exists():
            return HttpResponse('Does Not Exist')
        post = Post.objects.get(post_id = pk)
        serializer = PostSerializer(instance=post, data=data , many=False,partial=True)
        if serializer.is_valid():
            serializer.save()
            return HttpResponse('EDIT was successful!')
        return Response(serializer.errors)

class DeletePostAPIView(APIView):
    def delete(self,request,pk):
        if not Post.objects.filter(post_id=pk).exists():
            return HttpResponse('Does Not Exist')
        post_instance = Post.objects.get(post_id=pk)
        post_instance.delete()
        return HttpResponse('DELETE was successful!')

