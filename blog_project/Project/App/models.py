from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
# Create your models here.

STATUS = ((0, "Draft"), (1, "Published"))

class Post(models.Model):
  title =  models.CharField(max_length=200, unique=True)
  slug =   models.SlugField(max_length=200, unique=True)
  author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='blog_posts')
  posted_on = models.DateTimeField(auto_now_add=True)
  updated_on = models.DateTimeField(auto_now=True)
  content = models.TextField()
  status = models.IntegerField(choices=STATUS, default=0)
  image = models.FileField(null=True, blank=True)
  # image = models.ImageField(upload_to='blogs', default=None)
  is_deleted = models.BooleanField(default=False)

  class Meta:
    ordering = ['-posted_on']

  def __str__(self):
    return self.title
  
  def get_absolute_url(self):
        return reverse("post_detail", kwargs={"slug": str(self.slug)})
  
#   def get_create_url(self):
#         return reverse('post:create', kwargs={'id': self.id})

  def get_update_url(self):
        return reverse('post:update', kwargs={'id': self.id})

  def get_delete_url(self):
        return reverse('post:delete', kwargs={'id': self.id})
  
class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="comments")
    name = models.CharField(max_length=80)
    email = models.EmailField()
    body = models.TextField()
    posted_on = models.DateTimeField(auto_now_add=True)
    active = models.BooleanField(default=False)

    class Meta:
        ordering = ["posted_on"]

    def __str__(self):
        return "Comment {} by {}".format(self.body, self.name)