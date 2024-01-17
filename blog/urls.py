from . import views
from django.urls import path

urlpatterns = [
    path('', views.HomePage.as_view(), name='home'),
    path('user_post/', views.user_post, name='user_post'),
    path('<slug:slug>/', views.post_detail, name='post_detail'),
]
