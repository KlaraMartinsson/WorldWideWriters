from . import views
from django.urls import path

urlpatterns = [
    path('', views.HomePage.as_view(), name='home'),
    path('posts/', views.PostList.as_view(), name='post_list'),
    path('user_post/', views.user_post, name='user_post'),
    path('user_profile/', views.user_profile, name='user_profile'),
    path('<slug:slug>/', views.PostDetail.as_view(), name='post_detail'),
    path('saved_post/<slug:slug>/', views.PostSaved.as_view(), name='post_saved'),
    path('post/edit/<int:id>', views.post_edit, name='post_edit'),
    path('post/delete/<int:id>', views.post_delete, name='post_delete'),
    path('continent_posts/<int:continent>/', views.ContinentPosts.as_view(), name='continent_posts'),
]
