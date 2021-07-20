from django.urls import path, include
from rest_framework import routers

from api.views import *

router = routers.SimpleRouter()
router.register(r'posts', PostsViewSet)

urlpatterns = [
    path('posts/<int:post_id>/comments/',
         CommentList.as_view({'get': 'list', 'post': 'create'})),
    path('posts/<int:post_id>/comments/<int:comment_id>/',
         CommentDetail.as_view({'get': 'retrieve', 'put': 'update',
                                'patch': 'partial_update', 'delete': 'destroy'})),
    path('', include(router.urls)),
    path('follow/', FollowListCreate.as_view()),
    path('group/', GroupListCreate.as_view()),
]
