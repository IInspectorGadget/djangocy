from django import template

register = template.Library()

from ..models import *


@register.simple_tag
def getFriendId(user, profile):
    try:
        bol = bool(user.friends.get(id = profile.id))
    except User.DoesNotExist:
        bol = False
    return bol 


@register.simple_tag
def checkRequest(user, profile):
    try:
        bol = bool(profile.to_user.get(from_user = user.id))
    except FriendRequest.DoesNotExist:
        bol = False
    return bol

@register.simple_tag
def chekUserChat(chat, user):
    return chat.members.filter(username__exact = user)
# @register.simple_tag
# def chekUserChat(user, chatId):
#     chat = Chat.objects.get(id = chatId)
#     if user in chat.members.all():
#         return True
#     else: 
#         return False
