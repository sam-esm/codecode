from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from taggit.managers import TaggableManager
import os.path
from django.conf import settings
# Create your views here.
def generate_upload_path(instance, filename):
    return os.path.join(settings.STATIC_ROOT, 'blog/img/')

class PublishedManager(models.Manager):
    def get_queryset(self):
        # everey class in models have a defualt modelManager named objects
        # in python 3 we can use --> return super().get_queryset().filter(status='published')
        return super(PublishedManager,self).get_queryset().filter(status='published')


class Post(models.Model):
    STATUS_CHOICES = (
        ('draft','Draft'),
        ('published', 'Published'),
    )


    title = models.CharField(max_length=250)
    slug = models.SlugField(max_length=250,unique_for_date ='publish')
    author = models.ForeignKey(User,related_name="blog_posts")
    body = models.TextField()
    publish = models.DateField(default = timezone.now)
    created = models.DateTimeField(auto_now_add = True)
    updated = models.DateTimeField(auto_now = True)
    status = models.CharField(max_length = 10, choices=STATUS_CHOICES, default='draft')
    objects = models.Manager() #--> for use our defualt object manager
    published =  PublishedManager()
    tags = TaggableManager()
    images = models.ImageField(null=True,blank=True,width_field="width_field",height_field="height_field")
    width_field = models.IntegerField(default=0)
    height_field = models.IntegerField(default=0)
    class Meta:
        ordering = ('-publish',)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('blog:post_detail', args=[self.publish.year,
                                                self.publish.strftime('%m'),
                                                self.publish.strftime('%d'),
                                                self.slug])



class Comment(models.Model):
    post = models.ForeignKey(Post, related_name='comments')
    name = models.CharField('نام',max_length=80)
    email = models.EmailField('ایمیل')
    body = models.TextField('دیدگاه')
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=True)

    class Meta:
        ordering = ('created',)

        def __str__(self):
            return 'Comment by {} on {}'.format(self.name, self.post)
