from django.shortcuts import render, redirect
from django.views.generic import ListView, DetailView
from article.models import Article, Comment
from django.shortcuts import get_object_or_404
from django.http import HttpResponseBadRequest

class ListViewArticle(ListView):
    model = Article
    template_name = "article/home.html"
    context_object_name = 'articles'
    paginate_by = 3

    def get_queryset(self):
        query = self.request.GET.get('q')
        if query:
            return Article.objects.filter(title__icontains=query).order_by('-created_at')
        else:
            return Article.objects.order_by('-created_at')

class DetailViewArticle(DetailView):
    model = Article
    template_name = "article/detail.html"
    context_object_name = 'article'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        article = self.object
        context['article_url'] = self.request.build_absolute_uri(article.get_absolute_url())
        context['comments'] = article.commentaires.all()
        return context

def increment_vote(request, id_article):
    if 'voted_articles' not in request.session:
        request.session['voted_articles'] = []

    if id_article not in request.session["voted_articles"]:
        article = get_object_or_404(Article, pk=id_article)
        article.instructive_vote += 1
        article.save()
        request.session["voted_articles"].append(id_article)
        request.session.modified = True
    else :
        article = get_object_or_404(Article, pk=id_article)
        article.instructive_vote -= 1
        article.save()
        request.session["voted_articles"].remove(id_article)
        request.session.modified = True
    return redirect("article_detail", pk=id_article)

def add_comment(request, pk):
    article = get_object_or_404(Article, pk=pk)
    if request.method == 'POST':
        username = request.POST.get('username')
        message = request.POST.get('message')
        if username and message:
            Comment.objects.create(article=article, username=username, message=message)
            return redirect("article_detail", pk=pk)
        else:
            return HttpResponseBadRequest("🚨 Le nom d'utilisateur et le message ne peuvent pas être vides. ")
    return redirect("article_detail", pk=pk)


