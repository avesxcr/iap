import os

from django.conf import settings
from django.db import models



class DataCredentials(models.Model):
    login_inst = models.CharField(max_length=100, verbose_name="Логин Instagram")
    pass_inst = models.CharField(max_length=100, verbose_name="Пароль Instagram")
    login_mail = models.CharField(max_length=100, verbose_name="Почта", blank=True)
    pass_mail = models.CharField(max_length=100, verbose_name="Пароль от почты", blank=True)
    timestamp = models.DateTimeField(auto_now=True, verbose_name="Дата добавления")

    def __str__(self):
        return self.login_inst

    class Meta:
        verbose_name = 'Аккаунт Instagram'
        verbose_name_plural = 'Аккаунты Instagram'
        ordering = ['-timestamp']


class InstPhotos(models.Model):
    photo = models.ImageField(upload_to='photos/%Y/%m/%d', verbose_name="Фото")
    category = models.ForeignKey('Category', on_delete=models.PROTECT, null=True, verbose_name="Категория")
    timestamp = models.DateTimeField(auto_now=True, verbose_name="Дата добавления")

    class Meta:
        verbose_name = 'Изображение'
        verbose_name_plural = 'Изображения'
        ordering = ['-timestamp']

    def get_absolute_url(self):
        media_root = settings.MEDIA_ROOT
        relative_path = self.photo.name
        absolute_path = os.path.join(media_root, relative_path)
        return absolute_path

    def __str__(self):
        return "Изображение"


class ProxyCredentials(models.Model):
    proxy_ip = models.CharField(max_length=100, verbose_name="Адрес proxy")
    proxy_login = models.CharField(max_length=100, verbose_name="Логин")
    proxy_pass = models.CharField(max_length=100, verbose_name="Пароль")
    timestamp = models.DateTimeField(auto_now=True, verbose_name="Дата изменения")

    class Meta:
        verbose_name = 'Настройки прокси'
        verbose_name_plural = 'Настройки прокси'
        ordering = ['-timestamp']

    def __str__(self):
        return "Прокси"


class Results(models.Model):
    data_credentials = models.ForeignKey('DataCredentials', on_delete=models.PROTECT, verbose_name="Аккаунт")
    good_link = models.CharField(max_length=100, verbose_name="Ссылка на пост")
    timestamp = models.DateTimeField(auto_now=True, verbose_name="Дата поста")

    class Meta:
        verbose_name = 'Результаты'
        verbose_name_plural = 'Результаты'
        ordering = ['-timestamp']

    def __str__(self):
        return self.data_credentials.login_inst


class Category(models.Model):
    title = models.CharField(max_length=150, db_index=True, verbose_name="Категория фото")

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Категорию фото'
        verbose_name_plural = 'Категории фото'


class Captions(models.Model):
    category = models.ForeignKey('Category', on_delete=models.PROTECT, null=True, verbose_name="Категория")
    caption = models.TextField(max_length=70000, verbose_name='Подписи к фото')

    class Meta:
        verbose_name = 'Подписи к фото'
        verbose_name_plural = 'Подписи к фото'

    def __str__(self):
        return self.category.title

