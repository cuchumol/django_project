from django.contrib import admin
from django.urls import path, include

urlpatterns = [
  #  path('', views.post_list, name='post_list'),
  #  path('posts/<int:id>/', views.post_detail, name='post_detail'),
  #  path('posts/add/', views.post_edit, name='post_add'),
  #  path('posts/<int:id>/edit', views.post_edit, name='post_edit'),
    path('admin/', admin.site.urls),
    path('', include('blog.urls')),
    path('api-auth/', include('rest_framework.urls')),
    path('accounts/', include('django.contrib.auth.urls')),
]


#handler404='blog.views.handler404