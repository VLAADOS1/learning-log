from django.conf import settings
from django.db import models


class Topic(models.Model):
    text = models.CharField("Название темы", max_length=200)
    date_added = models.DateTimeField(auto_now_add=True)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    def __str__(self):
        return self.text


class Entry(models.Model):
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE, related_name="entries")
    text = models.TextField("Текст записи")
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.text[:50]
