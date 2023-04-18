from django.db import models

class HashData(models.Model):
    name = models.CharField(max_length=200, null=True)
    rollnum = models.IntegerField(null=True)
    mail = models.EmailField(null=True)
    phnum = models.IntegerField(null=True)
    dept = models.CharField(max_length=200, null=True)
    img = models.CharField(max_length=600, null=True)

    def __str__(self):
        return self.name
    
class LoginData(models.Model):
    username = models.CharField(max_length=200, null=True)
    password = models.CharField(max_length=200, null=True)

    def __str__(self):
        return self.username