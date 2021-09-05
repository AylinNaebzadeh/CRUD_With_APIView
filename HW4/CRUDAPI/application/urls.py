from django.urls import path
from . views import *
urlpatterns = [
    path('certainuserposts/<username>/',ListPostAPIView.as_view(),name='todo'),
    path('detail/<str:pk>/',PostDetailAPIView.as_view(),name='detail'),
    path('create',CreatePostAPIView.as_view(),name='create'),
    path('update/<str:pk>/',UpdatePostAPIView.as_view(),name='update'),
    path('delete/<str:pk>/',DeletePostAPIView.as_view(),name='delete'),
]