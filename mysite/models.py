from django.contrib.auth.models import User
from django.db import models


class GenderChoices(models.TextChoices):
    MALE = 'male', "Мужской"
    FEMALE = 'female', "Женский"


class RelationshipChoices(models.TextChoices):
    SINGLE = 'single', "Холост"
    IN_A_REL = 'in_a_rel', "В отношениях"
    ENGAGED = 'engaged', "Помолвлен(а)"
    MARRIED = 'married', "Женат/Замужем"
    IN_LOVE = 'in_love', "Влюблен(а)"
    COMPLICATED = 'complicated', "Все сложно"


class Profile(models.Model):
    user = models.OneToOneField(User, verbose_name="Пользователь", on_delete=models.CASCADE)
    avatar = models.FileField(verbose_name="Аватар", null=True, blank=True)
    team = models.TextField(verbose_name="Команда",max_length=500, blank=True, null=True)
    bio = models.TextField(verbose_name="О себе", max_length=500, blank=True, null=True)
    city = models.CharField(verbose_name="Город", max_length=50, blank=True, null=True, )
    birth_date = models.DateField(verbose_name="Дата рождения", null=True, blank=True)
    gender = models.CharField(verbose_name="Пол", choices=GenderChoices.choices, max_length=10)
    relationship = models.CharField(verbose_name="Статус отношений", choices=RelationshipChoices.choices, max_length=20)


class Post(models.Model):
    datetime = models.DateTimeField(verbose_name="Дата", auto_now_add=True)
    author = models.ForeignKey(User, verbose_name="Автор", on_delete=models.CASCADE, related_name="posts")
    text = models.CharField(verbose_name="Текст", max_length=1000, null=True, blank=True)
    image = models.FileField(verbose_name="Картинка", null=True, blank=True)

    class Meta:
        ordering = ["-datetime"]


class Comment(models.Model):
    datetime = models.DateTimeField(verbose_name="Дата", auto_now_add=True)
    author = models.ForeignKey(User, verbose_name="Автор", on_delete=models.CASCADE, related_name="comments")
    post = models.ForeignKey(Post, verbose_name="Пост", on_delete=models.CASCADE, related_name="comments")
    text = models.CharField(verbose_name="Текст", max_length=1000, null=True, blank=True)

    class Meta:
        ordering = ["datetime"]