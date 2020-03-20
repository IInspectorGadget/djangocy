from django.urls import path 
from . import views
from django.contrib.auth.decorators import login_required
from news.models import *
app_name = 'news'

urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('news/', views.NewsListView.as_view(), name='news'),
    path('news/<int:id>', views.NewsDetailView.as_view(), name='newsDetail'),
    path('news/<int:id>/add', views.NewsFormView.as_view(), name='newsAdd'),

    path('profile/<slug:username>/', views.ProfileDetailView.as_view(), name="profile"),
    path('profile/<slug:username>/edit/', views.ProfileFormView.as_view(), name ='edit'),
    path('profile/<slug:username>/add/', views.send_friend_request, name ='add'),
    path('profile/<slug:username>/accept/', views.accept_friend_request, name ='accept'),
    path('profile/<slug:username>/deny/', views.deny_friend_request, name ='deny'),
    path('profile/<slug:username>/<slug:friend>/delete/', views.delete_friend_request, name='deleteFriend'),
    path('profile/<slug:username>/chats/', views.ChatListView.as_view(), name='chats'),
    path('profile/<slug:username>/chats/<int:id>/', views.ChatDetailView.as_view(), name='chat'),
    #path('profile/<slug:username>/chats/<int:pk>/', views.room, name='chat'),

    path('profile/<slug:username>/chats/<int:pk>/submit', views.renderMessage, name='submitMessage'),
    

    path('register/', views.RegisterView.as_view(), name='register'),
    path('register/POST', views.registerPost, name='registerPost'),

    path('news/<int:pk>/like/', login_required(views.VotesView.as_view(model=News, vote_type=LikeDislike.LIKE)), name='article_like'),
    path('news/<int:pk>/dislike/', login_required(views.VotesView.as_view(model=News, vote_type=LikeDislike.DISLIKE)), name='article_dislike'),

]