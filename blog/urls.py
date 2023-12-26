
from django.urls import path, include
from blog import views
from rest_framework.routers import DefaultRouter
from .serializer import PostViewSet, CommentViewSet

urlpatterns = [
    path('', views.post_list, name='post_list'),
    path('posts/<int:id>/', views.post_detail, name='post_detail'),
    path('posts/add/', views.post_edit, name='post_add'),
    path('posts/<int:id>/publish/', views.post_publish, name='post_publish'),
    path('posts/<int:id>/edit', views.post_edit, name='post_edit'),
    path('posts/<int:id>/comment', views.add_comment, name='add_comment'),
    path('post/<int:id>/delete/', views.post_delete, name='post_delete'),
]


router = DefaultRouter()
router.register(r'posts', PostViewSet)
router.register(r'comments', CommentViewSet)

api_urlpatterns = [
    path('api/', include(router.urls)),
]

urlpatterns += api_urlpatterns
#handler404='blog.views.handler404