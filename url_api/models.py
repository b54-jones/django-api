from django.db import models

class URLInfo(models.Model):
    url = models.URLField(unique=True)
    domain_name = models.CharField(max_length=30)
    protocol = models.CharField(max_length=5)
    title = models.CharField(max_length=30)
    image = models.JSONField()
    stylesheets = models.IntegerField()

    def __str__(self):
        return self.url