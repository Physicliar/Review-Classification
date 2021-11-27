from django.db import models


class Application(models.Model):
    appId = models.CharField(max_length=255)
