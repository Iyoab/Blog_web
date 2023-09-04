from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User #Import user model for the author field

class Post(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    date_posted = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='blog_images/',null=True,blank=True)

    def __str__(self):
        return self.title


    def get_absolute_url(self):
        return reverse('post_detail', kwargs={'pk': self.pk})