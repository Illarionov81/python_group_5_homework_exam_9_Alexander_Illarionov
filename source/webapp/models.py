from django.contrib.auth import get_user_model
from django.db import models


class Gallery(models.Model):
    photo = models.ImageField(null=False, blank=False, upload_to='photo', verbose_name='photo')
    signature = models.CharField(max_length=2000, null=False, blank=False, verbose_name='Подпись')
    author = models.ForeignKey(get_user_model(), null=False, blank=False, on_delete=models.CASCADE,
                               verbose_name='Автор')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Время создания')

    def liked_by(self, user):
        favorites = self.favorites.filter(user=user)
        return favorites.count() > 0

    def __str__(self):
        return f'{self.author} - {self.signature}'

    class Meta:
        verbose_name = 'Gallery'
        verbose_name_plural = 'Gallery'




class Favorites(models.Model):
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE,
                             related_name='photo_favorites', verbose_name='Пользователь')
    photo = models.ForeignKey('webapp.Gallery', on_delete=models.CASCADE,
                              related_name='favorites', verbose_name='избранное')

    def __str__(self):
        return f'{self.user.username} - {self.photo.signature}'


    class Meta:
        verbose_name = 'Избранное'
        verbose_name_plural = 'Избранное'
