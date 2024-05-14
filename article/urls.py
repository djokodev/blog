from django.urls import path
from article.views import ListViewArticle, DetailViewArticle, increment_vote, add_comment

urlpatterns = [
    path("", ListViewArticle.as_view(), name="home"),
    path("article/<int:pk>/", DetailViewArticle.as_view(), name="article_detail"),
    path("increment_vote/<int:id_article>/", increment_vote, name="increment_vote"),
    path("add_comment/<int:pk>/", add_comment, name="add_comment"),
]