from django.db import models
from django.conf import settings
from django.utils import timezone
from django.urls import reverse
from .managers import PostManager, PostPushManager
from django.template.defaultfilters import truncatewords

class Post(models.Model):
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    preview_text = models.TextField()
    title = models.CharField(max_length=200)
    text = models.TextField()
    created_date = models.DateTimeField(default=timezone.now)
    published_date = models.DateTimeField(null=True, blank=True)
    is_published = models.BooleanField(default=False)

    objects = PostManager()
    published = PostPushManager()
    

    def publish(self):
        self.published_date = timezone.now()
        self.is_published = True  
        self.save()

    def save(self, *args, **kwargs):
        self.preview_text = truncatewords(self.text, 10)
        super().save(*args, **kwargs)


    class Meta:
        verbose_name = 'Запись в блоге'
        verbose_name_plural = 'Записи в блоге'

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('post_detail', args=[str(self.id)])


    def get_text_preview(self):
        return truncatewords(self.text, 10)



class Comment(models.Model):
    post = models.ForeignKey('blog.Post', on_delete=models.CASCADE, related_name='comments')
    author = models.CharField(max_length=200)
    text = models.TextField()
    created_date = models.DateTimeField(default=timezone.now)
    approved_comment = models.BooleanField(default=False)

    #    return True if self.published_date else False

    def approve(self):
        self.approved_comment = True
        self.save()

    class Meta:
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'

    def __str__(self):
        return self.title


