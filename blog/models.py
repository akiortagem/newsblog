from django.db import models
from django.contrib.auth.models import User

DEFAULT_AUTHOR_ID = 1

class PostStatus:
	status=(
		('DR', 'Draft'),
		('OK', 'Ok to publish'),
		)

class Blog(models.Model):
    title = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=100, unique=True)
    body = models.TextField()
    posted = models.DateTimeField(db_index=True, auto_now_add=True)
    status = models.CharField(max_length=2, choices=PostStatus.status, default='OK')
    publish_on = models.DateField()
    picture = models.ImageField(upload_to = 'media/', default = 'media/no-img.jpg')
    category = models.ForeignKey('blog.Category')
    author = models.ForeignKey(User)

    class Meta:
        ordering = ['-id']
        verbose_name = 'Blog Post'

    class ViewMeta:
        table_columns = [
            'title',
            'author',
            'posted',
            'category',
            'status',

        ]
        view_name = 'Blog Post'

    @property
    def body_shortened(self):
        return str(self.body)[0:200]


class MessageStatus:
    status=(
        ('UR','unread'),
        ('R','read'),
        )

class Message(models.Model):
    class Meta:
        permissions = (
                ('can_view_message', 'Can view message in dashboard'),
            )
        ordering = ['-id']
        
    name=models.CharField(max_length=100)
    phone=models.CharField(max_length=100)
    email=models.CharField(max_length=100)
    subject=models.CharField(max_length=140)
    message=models.TextField()
    date=models.DateTimeField(db_index=True, auto_now_add=True)
    status=models.CharField(max_length=2, choices=MessageStatus.status, default='UR')

    class ViewMeta:
        table_columns = [
            'name',
            'email',
            'subject',
            'date',
        ]
        view_name='Message'

class Category(models.Model):
    title = models.CharField(max_length=100, db_index=True)
    slug = models.SlugField(max_length=100, db_index=True)
    author = models.ForeignKey(User)

    def __unicode__(self):
        return self.title

class Image(models.Model):
    class Meta:
        ordering = ['-id']
        verbose_name = 'Image'

    title = models.CharField(max_length=100, unique=True)
    image = models.ImageField(upload_to = 'media/', default = 'media/no-img.jpg')
    caption = models.CharField(max_length=140, unique=True)
    uploaded_by = models.ForeignKey(User, null=True, blank=True)
    date = models.DateTimeField(db_index=True, auto_now_add=True)

    def __unicode__(self):
        return self.title;

class ImageGallery(models.Model):
    class Meta:
        ordering = ['-id']
        verbose_name = 'Image Gallery'

    title = models.CharField(max_length=100, unique=True)
    images = models.ManyToManyField(
        Image
        )
    created_by = models.ForeignKey(User)
    date = models.DateTimeField(db_index=True, auto_now_add=True)
    
    def __unicode__(self):
        return self.title;