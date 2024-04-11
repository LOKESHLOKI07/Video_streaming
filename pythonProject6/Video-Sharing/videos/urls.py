from django.contrib import admin
from django.urls import path, include
from rest_framework import routers
from .views import (video_list, video_detail, video_search, video_create,
                    video_update, video_delete, user_profile, register, login_view, VideoViewSet,
                    video_stream, test, video_only, oee_data, oee_data_filtered, ProductionLogViewSet)

# Define router for REST API
router = routers.DefaultRouter()
router.register(r'videos', VideoViewSet)
router.register(r'production-logs', ProductionLogViewSet)  # Add this line

urlpatterns = [
    path('video-list', video_list, name='video-list'),
    path('api/', include(router.urls)),
    path('videos/<int:pk>/', video_detail, name='video-detail'),
    path('videos/search/', video_search, name='video-search'),
    path('videos/create/', video_create, name='video-create'),
    path('videos/<int:pk>/update/', video_update, name='video-update'),
    path('videos/<int:pk>/delete/', video_delete, name='video-delete'),
    path('profile/', user_profile, name='user-profile'),
    path('register/', register, name='register'),
    path('login/', login_view, name='login'),
    path('video_stream/', video_stream, name='video-stream'),
    path('', test, name='test'),
    path('video_only/', video_only, name='video_only'),
    path('oee-data/', oee_data, name='oee-data'),
    path('oee-data-filtered/', oee_data_filtered, name='oee-data-filtered'),
]

