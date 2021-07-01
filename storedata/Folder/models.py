from django.db import models

from django.utils import timezone


from storedata.models import NewUser


class Folder(models.Model):
    user = models.ForeignKey(NewUser, on_delete=models.CASCADE)
    name = models.CharField(required=True)
    created = models.DateTimeField(auto_now_add=True, editable=False)
    updated = models.DateTimeField(auto_now=True, editable=True)

    def __str__(self):
        return self.headline

    class Meta:
        ordering = ['headline']
