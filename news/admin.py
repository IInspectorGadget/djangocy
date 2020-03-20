from django.contrib import admin
from .models import *
# Register your models here
from django.contrib.auth.admin import UserAdmin
from .forms import CustomUserCreationForm, CustomUserChangeForm
#в админке отоброжение
class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = User
    fieldsets = (
        (None, {'fields': ('username', 'password')}),

        (('Personal info'), {'fields': ('first_name', 'last_name','patronymic', 'email', 'image', 'phone','dateBirth', 'addres', 'gender', 'friends', 'organization', 'skype')}),
        (('Permissions'), {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions'),}),
        (('UrlsSeting'), {'fields': ('slug',),}),
        (('Privacy'), {'fields': ('showRealName','showUsername')}),
        (('Important dates'), {'fields': ('last_login', 'date_joined')}),
    )

# class FriendAdmin(admin.ModelAdmin):
#     model = Friend
#     fieldsets = (
#         (None, {'fields': ('users', )}),
#     )


admin.site.register(News)
admin.site.register(User, CustomUserAdmin)
admin.site.register(FriendRequest)
admin.site.register(Chat)
admin.site.register(Message)

admin.site.register(LikeDislike)