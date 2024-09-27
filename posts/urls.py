from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import PostViewSet, CommentViewSet, FeedView, LikeViewSet

router = DefaultRouter()
router.register(r'posts', PostViewSet)
router.register(r'comments', CommentViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('posts/<int:post_pk>/comments/', CommentViewSet.as_view({'get': 'list', 'post': 'create'}), name='post-comments'),
    path('posts/<int:post_pk>/comments/<int:pk>/', CommentViewSet.as_view({'get': 'retrieve', 'put': 'update', 'patch': 'partial_update', 'delete': 'destroy'}), name='post-comment-detail'),
    path('posts/<int:post_id>/like/', PostViewSet.as_view({'post': 'like', 'delete': 'unlike'}), name='post-like'),
    path('posts/<int:post_id>/comments/', CommentViewSet.as_view({'get': 'list', 'post': 'create'}), name='post-comments'),
    path('posts/<int:post_id>/like/', PostViewSet.as_view({'post': 'like', 'delete': 'unlike'}), name='post-like'),
    path('feed/', FeedView.as_view(), name='feed'),
      path('posts/<int:pk>/like/', LikeViewSet.as_view({'post': 'create', 'delete': 'destroy'}), name='post-like'),
    path('posts/<int:pk>/unlike/', LikeViewSet.as_view({'post': 'create', 'delete': 'destroy'}), name='post-unlike'),
]