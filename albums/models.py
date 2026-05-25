from django.contrib.auth import get_user_model
from django.db import models
from cloudinary.models import CloudinaryField

User = get_user_model()


class Album(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='albums')
    title = models.CharField(max_length=180)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.title

    def can_edit(self, user):
        if not user.is_authenticated:
            return False
        return user == self.owner or user.is_superuser or user.groups.filter(name='Album Admin').exists()


class Photo(models.Model):
    album = models.ForeignKey(Album, on_delete=models.CASCADE, related_name='photos')
    title = models.CharField(max_length=180)
    caption = models.TextField(blank=True)
    image = CloudinaryField('image')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.title

    def can_edit(self, user):
        return self.album.can_edit(user)
