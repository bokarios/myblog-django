from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from django.utils import timezone
from datetime import datetime
from django.utils.text import slugify
from ckeditor_uploader.fields import RichTextUploadingField
from django.contrib.contenttypes.fields import GenericRelation
from hitcount.models import HitCount


# Posts mmodel
class Post(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='posts')
    title = models.CharField(max_length=100)
    slug = models.SlugField(default='', editable=False, max_length=100)
    content = RichTextUploadingField()
    image = models.ImageField(default='default.png', upload_to='post_pics')
    hit_count_generic = GenericRelation(HitCount, object_id_field='object_pk', related_query_name='hit_count_generic_relation')
    created_at = models.DateTimeField(default=datetime.now, blank=True)
    updated_at = models.DateTimeField(default=datetime.now, blank=True)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('post-detail', kwargs={'pk': self.pk, 'slug': self.slug})

    def save(self, *args, **kwargs):
        self.updated_at = datetime.now()

        if not self.pk:
            value = self.title
            self.slug = slugify(value, allow_unicode=True)

        super(Post, self).save(*args, **kwargs)
        return self

# Comments model
class Comment(models.Model):
    article = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comments')
    comment = models.TextField()
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f'{self.user.username} comment on ({self.article.title})'

# Likes model
class Like(models.Model):
    article = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='likes')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='likes')
    created_at = models.DateTimeField(default=datetime.now, blank=True)

    def __str__(self):
        return f'{self.user.username} likes ({self.article.title})'

# Dilikes model
class Dislike(models.Model):
    article = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='dislikes')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='dislikes')
    created_at = models.DateTimeField(default=datetime.now, blank=True)

    def __str__(self):
        return f'{self.user.username} dislikes ({self.article.title})'
