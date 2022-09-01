from django.db import models

# Create your models here.
class Post(models.Model):
    created = models.DateTimeField(auto_now_add=True)           #auto_now_add znaci da ce sam da se popunjava
    title = models.CharField(max_length=100, blank=False)       #ostala 3 atributa mi popunjavamo
    content = models.TextField()
    author = models.CharField(max_length=100, blank=False)
    owner = models.ForeignKey('auth.user', related_name='posts',on_delete=models.CASCADE)    #dodato nakon kreiranja superusera, uvezujemo ovako klasu Post sa userom

    class Meta:
        ordering = ['created']               