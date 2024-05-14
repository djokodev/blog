from django.db import models
from ckeditor.fields import RichTextField
from ckeditor_uploader.fields import RichTextUploadingField
from django.urls import reverse
import locale


class Article(models.Model):
    title = models.CharField(max_length=150)
    content = RichTextUploadingField()
    image = models.ImageField()
    instructive_vote = models.IntegerField(default=0)
    reading_time_min = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
    
    def formatted_date(self):
        locale.setlocale(locale.LC_TIME, 'fr_FR.UTF-8')
        return self.created_at.strftime("%d %B %Y") 
    
    def get_absolute_url(self):
        return reverse('article_detail', kwargs={'pk': self.pk})
    
class Comment(models.Model):
    article = models.ForeignKey(Article, on_delete=models.CASCADE, related_name="commentaires")
    username = models.CharField(max_length=100)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Commentaire de {self.username} le {self.created_at.strftime("%d/%m/%Y %H:%M:%S")}"
