from django.urls import reverse_lazy, reverse
from django.shortcuts import redirect
from django.views import View
from django.contrib import messages
from django.views.generic.detail import SingleObjectMixin
from django.views.generic import ListView, DetailView, FormView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin

from .models import Article, Comment
from .forms import CommentForm


# Create your views here.
class ArticleListView(LoginRequiredMixin, ListView):
    model = Article
    template_name = "articles/article_list.html"
    context_object_name = "articles"


class ArticleEditView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Article
    template_name = "articles/article_edit.html"
    fields = ["title", "body"]
    context_object_name = "article"

    def test_func(self):
        return self.get_object().author == self.request.user


class ArticleDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Article
    template_name = "articles/article_delete.html"
    success_url = reverse_lazy("article_list")

    def test_func(self):
        return self.get_object().author == self.request.user


class ArticleCreateView(LoginRequiredMixin, CreateView):
    model = Article
    template_name = "articles/article_create.html"
    fields = ["title", "body"]

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class ArticleDetailView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        view = CommentGet.as_view()
        return view(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        view = CommentPost.as_view()
        return view(request, *args, **kwargs)


class CommentGet(DetailView):
    model = Article
    template_name = "articles/article_detail.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["form"] = CommentForm()
        return context


class CommentPost(SingleObjectMixin, FormView):
    model = Article
    form_class = CommentForm
    template_name = "articles/article_detail.html"

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        # prevent users from commenting on their own posts.
        if self.request.user == self.object.author:
            messages.error(request, "You cannot comment on your own post.")
            return redirect("article_detail", pk=self.object.pk)

        # prevent a user from making more than one comment.
        if Comment.objects.filter(author=self.request.user, article=self.object):
            messages.error(request, "You have already commented on this post.")
            return redirect("article_detail", pk=self.object.pk)

        return super().post(request, *args, **kwargs)

    def form_valid(self, form):
        comment = form.save(commit=False)
        comment.article = self.object
        comment.author = self.request.user
        comment.save()
        return super().form_valid(form)

    def get_success_url(self):
        article = self.object
        return reverse("article_detail", kwargs={"pk": article.pk})
