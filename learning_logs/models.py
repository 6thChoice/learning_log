import datetime

from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Topic(models.Model):
    # 用于储存主题
    text = models.CharField(max_length=250)
    date_added = models.DateTimeField(auto_now_add=True)
    owner = models.ForeignKey(User,on_delete=models.CASCADE)

    def __str__(self):
        return self.text

class entry(models.Model):
    # 用于储存与每一条主题相关联的内容
    topic = models.ForeignKey(Topic,on_delete=models.CASCADE) # 储存关联性
    text = models.TextField()
    date_added = models.DateTimeField(auto_now_add=True)
    owner = models.ForeignKey(User,on_delete=models.CASCADE)

    def __str__(self):
        if len(self.text)<50:
            return self.text
        else:
            return self.text[:50]+'...'