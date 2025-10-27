import uuid

from django.db import models
from django.conf import settings
from django.urls import reverse


# Create your models here.
class Article(models.Model):
    article_id = models.UUIDField(
        primary_key=True, unique=True, default=uuid.uuid4, editable=False
    )
    title = models.CharField(max_length=200)
    body = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    class Meta:
        ordering = ("-created_at",)

    def __str__(self):
        return self.title.title()

    def get_absolute_url(self):
        return reverse("article_detail", kwargs={"pk": self.pk})

    @property
    def snippet(self):
        """Get the first five word and display them with trailing eplipses"""
        words = self.body.split()
        snippet = " ".join(words[:5])
        return snippet + "..."
