from django.shortcuts import render
from .models import News

from django.views.generic.base import View
# Create your views here.
from .forms import UserForm, CustomUserCreationForm
from .models import *
from django.contrib.auth.hashers import make_password
from django.http import HttpResponseRedirect , Http404
from django.urls import reverse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404, redirect, render

from django.views.generic import DetailView
from django.views.generic.edit import FormView, UpdateView, CreateView
from django.views.generic.list import ListView
from django.views.generic.detail import BaseDetailView
from django.http import HttpResponse, JsonResponse
from news.forms import NewsAddForm, ProfileEditForm
from django.forms.models import model_to_dict
from django.core.serializers import get_serializer
class IndexView(View):
    # login_url = 'accounts/login/'
    # redirect_field_name = 'huy'
    def get(self, request):
        news_list = News.objects.all()[:5]
        context = {'news_list': news_list}
        return render(request,'index.html', context)


class NewsListView(ListView):
    model = News
    template_name = 'news.html'
    context_object_name = 'news'

class NewsDetailView(DetailView):
    model = News
    template_name = "newsDetail.html"
    pk_url_kwarg = 'id'
    context_object_name = 'new'

class NewsFormView(CreateView):
    model = News
    form_class = NewsAddForm
    template_name = 'newsAdd.html'
    slug_url_kwarg = 'id'
    def form_valid(self, form):
        news = form.save(commit=False)
        news.author = self.request.user
        news.save()
        # News.objects.create(**form.cleaned_data)
        return redirect(self.get_success_url())
    def get_success_url(self):
        return reverse('news:news')

class ProfileDetailView(DetailView):
    model = User
    template_name = 'profile.html'
    slug_url_kwarg = 'username'
    context_object_name = 'profile'

class ProfileFormView(UpdateView):
    model = User
    slug_url_kwarg = 'username'
    template_name = 'profileForm.html'
    form_class = ProfileEditForm

    
    def get_success_url(self):
        username = self.kwargs['username']
        return reverse('news:profile', kwargs={'username' : username.lower()})


####################################################################################
class ChatListView(ListView):
    model = Chat
    template_name = 'chat.html'
    context_object_name = 'chats'

class ChatDetailView(DetailView):
    model = Chat
    template_name = 'room.html'
    context_objects_name = 'chat' 
    pk_url_kwarg = 'id'

    
# def room(request,username ,pk):
#     return render(request, 'chat/room.html', {
#         'room_name': pk
#     })


import json
def renderMessage(request, username, pk):
    # для axios
    # data = json.loads(request.body)
    # id = data['my']
    # для Jquery
    mes = request.POST.get('message')
    id = request.POST.get('id')
    message = Message()
    user = User.objects.get(id = id)
    print(username)
    username = user.username
    message.author = user
    message.message = mes
    message.chat_id = 1
    message.save()
    image = user.image.url
    return JsonResponse({'message' : model_to_dict(message), 'username': username, 'image': image }, safe=False)
    # return HttpResponse("success", content_type='text/html')



        # from django.db import models
        # if isinstance(f, models.ImageField):
        #     data[f.name] = str(f.value_from_object(instance))
        #     continue

def send_friend_request(request, username):
    profile = get_object_or_404(User, slug=username)
    check = profile.friends.filter(username = request.user.username)
    if (request.user.id != profile.id) and (not check):
        frequest, created = FriendRequest.objects.get_or_create(from_user=request.user,to_user=profile)
    return HttpResponseRedirect(reverse('news:profile', kwargs= {'username' : username.lower()}))

def accept_friend_request(request, username):
    from_user = get_object_or_404(User, slug=username)
    frequest = FriendRequest.objects.filter(from_user=from_user, to_user=request.user).first()
    if frequest:
        user1 = frequest.to_user
        user2 = from_user
        user1.friends.add(user2.id)
        user2.friends.add(user1.id)
        frequest.delete()
    return HttpResponseRedirect(reverse('news:profile', kwargs= {'username' : request.user.username.lower()}))



def deny_friend_request(request, username):
	from_user = get_object_or_404(User, slug=username)
	frequest = FriendRequest.objects.filter(from_user=from_user, to_user=request.user).first()
	frequest.delete()
	return HttpResponseRedirect(reverse('news:profile', kwargs= {'username' : request.user.username.lower()}))

def delete_friend_request(request, username, friend):
    if request.user.slug == username:
        user = get_object_or_404(User, slug=username)
        friend = user.friends.get(slug = friend)
        user.friends.remove(friend)
        friend.friends.remove(user)
    return HttpResponseRedirect(reverse('news:profile', kwargs= {'username' : request.user.username.lower()}))






####################################################################################

class RegisterView(View):
    
    def get(self, request):
        userform = UserForm()
        context = {
            "form": userform
        }
        return render(request,'registerForm.html', context)

def registerPost(request):
    # news_list = News.objects.all()[:5]
    # context = {'news_list': news_list,}

    # получаю данные и файлы  из формы
    userform = UserForm(request.POST, request.FILES)
    # проверяю валидность данных
    if userform.is_valid():
        # если есть файл с именем image то присваивается название файла
        #if 'image' in request.FILES:
            #userform.image = request.FILES['image']
        userform.save(commit=True)
        return HttpResponseRedirect(reverse('news:index'))
    else:
        print(userform.errors)
        return render(request, 'registerForm.html', {'form': userform})


class VotesView(View):
    model = None    # Модель данных - Статьи или Комментарии
    vote_type = None # Тип комментария Like/Dislike
    
    def post(self, request, pk):
        # берём нужную модель
        obj = self.model.objects.get(pk=pk)
        print(ContentType.objects.get_for_model(obj))
        # GenericForeignKey не поддерживает метод get_or_create
        try:
            #получаем модель у которой content_type news с id и id (шобы изменить данные)
            likedislike = LikeDislike.objects.get(content_type=ContentType.objects.get_for_model(obj), object_id=obj.id, user=request.user)
            if likedislike.vote is not self.vote_type:
                likedislike.vote = self.vote_type
                likedislike.save(update_fields=['vote'])
                result = True
            else:
                likedislike.delete()
                result = False
        except LikeDislike.DoesNotExist:
            obj.votes.create(user=request.user, vote=self.vote_type)
            result = True
 
        return HttpResponse(
            json.dumps({
                "result": result,
                "like_count": obj.votes.likes().count(),
                "dislike_count": obj.votes.dislikes().count(),
                "sum_rating": obj.votes.sum_rating()
            }),
            content_type="application/json"
        )