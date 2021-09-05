from django.db import models

# Create your models here.


class Post(models.Model):
    post_id = models.AutoField(primary_key=True)
    username = models.CharField(max_length=40 , unique=True,null=True,blank=True)
    message = models.CharField(max_length=200 , null=True , blank=True)
    date_created = models.DateTimeField(auto_now_add=True)
    post_photo = models.ImageField(null = True , blank = True,upload_to='postimages')

    def __str__(self):
        return self.message
