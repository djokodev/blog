from django.conf import settings
from django.db import models
from django.utils import timezone
from django.urls import reverse


# Gestionnaire personnalisé pour récupérer toutes les publications ayant le statut PUBLISHED.
class PublishedManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(status=Post.Status.PUBLISHED)


class Post(models.Model):

    objects = models.Manager()
    published = PublishedManager()

    class Status(models.TextChoices):
        DRAFT = "DF", "DRAFT"
        PUBLISHED = "PB", "PUBLISHED"

    title = models.CharField(max_length=250)

    # unique_for_date="publish": Si vous avez un article avec le slug "mon-article" publié le 1er janvier 2023, et que vous essayez de publier un autre article avec le même slug "mon-article" le même jour (1er janvier 2023), Django vous empêchera de le faire.
    slug = models.SlugField(max_length=250, unique_for_date="publish")
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="blog_posts"
    )
    body = models.TextField()
    publish = models.DateTimeField(default=timezone.now)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=2, choices=Status, default=Status.DRAFT)

    class Meta:
        ordering = ["-publish"]
        indexes = [
            models.Index(fields=["-publish"]),
        ]

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("blog:post_detail", args=[self.id])
