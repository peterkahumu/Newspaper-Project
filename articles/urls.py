from django.urls import path
from .views import (
    ArticleListView,
    ArticleDetailView,
    ArticleEditView,
    ArticleDeleteView,
    ArticleCreateView,
)

urlpatterns = [
    path("", ArticleListView.as_view(), name="article_list"),
    path("<uuid:pk>/", ArticleDetailView.as_view(), name="article_detail"),
    path("<uuid:pk>/edit/", ArticleEditView.as_view(), name="article_edit"),
    path("<uuid:pk>/delete/", ArticleDeleteView.as_view(), name="article_delete"),
    path("new/", ArticleCreateView.as_view(), name="article_create"),
]
