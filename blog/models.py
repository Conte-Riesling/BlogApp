from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User


class PublishedManager(models.Manager): 
    def get_queryset(self):
        return super().get_queryset()\
    .filter(status=Post.Status.PUBLISHED)


class Post(models.Model):

    class Status(models.TextChoices):
        DRAFT = 'DF', 'Draft'
        PUBLISHED = 'PB', 'Published'
    """Класс Status позволяет управлять статусом постов блога Draft
    (черновик) Published (опубликован)"""

    title = models.CharField(max_length=250)
    slug = models.SlugField(max_length=250)
    author = models.ForeignKey(User,
                               on_delete=models.CASCADE,
                               related_name='blog_posts')
    body = models.TextField()

    """Дата, время публикации и обновления  поста"""
    publish = models.DateTimeField(default=timezone.now)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=2,
                              choices=Status.choices,
                              default=Status.DRAFT)
    
    objects = models.Manager() # менеджер, применяемый по умолчанию 
    published = PublishedManager() # конкретно-прикладной менеджер


    """Meta-класс определяет метаданные модели.
    Атрибут ordering, сообщающий Django, что он 
    должен сортировать результаты по полю publishю
    indexes определяет индекс по полю publish"""

    class Meta:
        ordering = ['-publish']
        indexes = [
            models.Index(fields=['-publish']),
        ]

    def __str__(self):
        return self.title
    
    