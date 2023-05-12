from django.db import models

NULLABLE = {'null': True, 'blank': True}


class Post(models.Model):
    """
    Модель, описывающая пост в блоге
    """
    title = models.CharField(max_length=255, unique=True, verbose_name='Заголовок')
    slug = models.SlugField(max_length=50, blank=True, verbose_name='URL')
    content = models.TextField(verbose_name='Содержание')
    preview = models.ImageField(upload_to='posts/', verbose_name='Изображение (превью)', **NULLABLE)
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
