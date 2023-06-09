from django.db import models

# Create your models here.
class Crawling(models.Model):
    press = models.CharField(max_length=10, null=True)
    title = models.CharField(max_length=25, null=True)
    article = models.TextField()

    def __str__(self):
        return self.title

class Summary(models.Model):
    text = models.TextField()

    def __str__(self):
        return self.text


class Godsummary(models.Model):
    press = models.CharField(max_length=10, null=True)
    title = models.TextField()
    category = models.CharField(max_length=10, null=True)
    article = models.TextField()
    datetime = models.DateTimeField()
    link = models.TextField()



