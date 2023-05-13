from django.conf import settings
from django.core.mail import send_mail
from django.db import models
from slugify import slugify


class Post(models.Model):
    """
    Модель, описывающая пост в блоге
    """
    title = models.CharField(max_length=255, unique=True, verbose_name='Заголовок')
    slug = models.SlugField(max_length=255, blank=True, verbose_name='URL')
    content = models.TextField(verbose_name='Содержание')
    preview = models.ImageField(upload_to='posts/', verbose_name='Изображение (превью)', default='posts/default.jpg')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    published = models.BooleanField(verbose_name='Опубликован', default=True)
    views_count = models.PositiveIntegerField(default=0, verbose_name='Количество просмотров')

    class Meta:
        verbose_name = 'Пост'
        verbose_name_plural = 'Посты'
        db_table = 'posts'
        ordering = ['created_at']

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if self.pk:
            if self.title != Post.objects.get(id=self.id).title:
                self.slug = slugify(self.title)
        else:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def increment_view_count(self):
        self.views_count += 1
        self.save()

        if self.views_count == 100:
            send_mail(
                subject='Поздравляем с достижением!',
                message=f'Статья "{self.title}" достигла 100 просмотров!',
                from_email=settings.EMAIL_HOST_USER,
                recipient_list=[settings.EMAIL_HOST_USER]
            )

    def make_unpublished(self):
        self.published = False
        self.save()
