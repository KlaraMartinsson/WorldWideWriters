from . import views
from django.urls import path

urlpatterns = [
    path('', views.HomePage.as_view(), name='home'),
    path('user_post/', views.user_post, name='user_post'),
    path('<slug:slug>/', views.post_detail, name='post_detail'),
    path("post/edit/<int:id>", views.post_edit, name="post_edit"),
    path("post/delete/<int:id>", views.post_delete, name="post_delete"),
]
