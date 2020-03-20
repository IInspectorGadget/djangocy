import datetime

from ckeditor_uploader.fields import RichTextUploadingField
from django.contrib.auth.models import AbstractUser
from django.core.exceptions import NON_FIELD_ERRORS
from django.core.validators import RegexValidator
from django.db import models
from django.template.defaultfilters import slugify
from django.utils import dateformat, timezone
from django.utils.translation import gettext_lazy as _

from mysite import settings
from django.contrib.contenttypes.models import ContentType


# Create your models here.
class User(AbstractUser):
    image = models.ImageField('фото',upload_to='UserAvatars', default = 'UserAvatars/default.png')
    slug = models.SlugField(default = '')
    patronymic = models.CharField('patronymic', max_length=30, blank=True)
    
    dateBirth = models.DateField('дата рождения',blank=True, null=True)
# контактные данные (- email)
    phone_validator = RegexValidator('^((8|\+7)[\- ]?)?(\(?\d{3}\)?[\- ]?)?[\d\- ]{7,10}$', message="Введите правильный номер.")
    
    phone = models.CharField('телефон',validators=[phone_validator],max_length = 30, null=True, blank=True)

    skype = models.CharField('скайп', max_length = 30, blank=True, null=True)
    

    addres = models.TextField('адресс',max_length = 200,blank=True, null=True)
    organization = models.CharField('название организации', max_length = 100, blank=True, null=True)
    

    friends = models.ManyToManyField("User", blank=True)
    
    showUsername = models.BooleanField(default= False)
    showRealName = models.BooleanField(default= False)

    GENDER_CHOICES = (
        ('М', 'Мужской'),
        ('Ж', 'Женский'),
    )
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, null=True)

    def save(self, *args, **kwargs):
        if self.slug == '':
            self.slug = slugify(self.username)
        super().save(*args, **kwargs)
    

class Chat(models.Model):
    DIALOG = 'D'
    CHAT = 'C'
    CHAT_TYPE_CHOICES = (
        (DIALOG, ('Dialog')),
        (CHAT, ('Chat'))
    )
    last_message_date = models.DateTimeField("Дата сообщения", null=True, blank=True)
    type = models.CharField(
        'Тип',
        max_length=1,
        choices=CHAT_TYPE_CHOICES,
        default=DIALOG
    )
    members = models.ManyToManyField(User, verbose_name="Участник")

    def __str__(self):
        if self.type == 'D':
            d=''
            for member in self.members.all():
                d += member.username + '\n'
            return d
        else: 
            return super().__str__()
    class Meta:
        ordering = ['-last_message_date']


class Message(models.Model):
    chat = models.ForeignKey(Chat, verbose_name="Чат", on_delete=models.CASCADE)
    author = models.ForeignKey(User, verbose_name = "Пользователь", on_delete=models.CASCADE)
    message = models.TextField("Сообщение")
    pub_date = models.DateTimeField("Дата сообщения", default = timezone.now)
    is_related = models.BooleanField("Прочитано", default= False)

    class Meta:
        ordering = ['pub_date']

    def __str__(self):
        return self.message


    # def getTime(self):
    #     d = self.pub_date.strftime('%B')
    #     formatted_date = dateformat.format(d, settings.DATE_FORMAT)
    #     return formatted_date


class FriendRequest(models.Model):
    to_user = models.ForeignKey(User, related_name='to_user', on_delete=models.CASCADE)
    from_user = models.ForeignKey(User, related_name='from_user', on_delete=models.CASCADE)

    def __str__(self):
        return "From {}, to {}".format(self.from_user.username, self.to_user.username)


from django.contrib.contenttypes.fields import GenericForeignKey, GenericRelation

class News(models.Model):
    title = models.CharField(max_length = 50)
    small_text = RichTextUploadingField(config_name='smallText')
    text = RichTextUploadingField()
    votes = GenericRelation('LikeDislike', related_query_name='news')
    date_pub = models.DateTimeField(auto_now=False, default = timezone.now)
    image = models.ImageField(default="")
    author = models.ForeignKey(User, blank=True, on_delete=models.CASCADE, null=True)
    def __str__(self):
        return self.title

from django.db.models import Sum

class LikeDislikeManager(models.Manager):
    use_for_related_fields = True
 
    def likes(self):
        # Забираем queryset с записями больше 0
        return self.get_queryset().filter(vote__gt=0)
 
    def dislikes(self):
        # Забираем queryset с записями меньше 0
        return self.get_queryset().filter(vote__lt=0)
 
    def sum_rating(self):
        # Забираем суммарный рейтинг
        return self.get_queryset().aggregate(Sum('vote')).get('vote__sum') or 0

    # def articles(self):
    #     return self.get_queryset().filter(content_type__model='da').order_by('-news__date_pub')


class LikeDislike(models.Model):
    LIKE = 1
    DISLIKE = -1
 
    VOTES = (
        (DISLIKE, 'Не нравится'),
        (LIKE, 'Нравится')
    )
 
    vote = models.SmallIntegerField(verbose_name=_("Голос"), choices=VOTES)
    user = models.ForeignKey(User, verbose_name=_("Пользователь"), on_delete=models.CASCADE)
 
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey()
 
    objects = LikeDislikeManager()


 
 
