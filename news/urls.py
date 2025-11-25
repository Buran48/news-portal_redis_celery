from django.urls import path
from .test_views import TestCeleryView
from .views import (
    NewsList, NewsDetail, ArticlesList, ArticleDetail,
    NewsCreate, ArticleCreate, NewsUpdate, ArticleUpdate,
    NewsDelete, ArticleDelete,
    NewsSearch,
    subscribe, unsubscribe
)

urlpatterns = [
    path('', NewsList.as_view(), name='news_list'),
    path('<int:pk>/', NewsDetail.as_view(), name='news_detail'),

    path('search/', NewsSearch.as_view(), name='news_search'),

    path('articles/', ArticlesList.as_view(), name='articles_list'),
    path('articles/<int:pk>/', ArticleDetail.as_view(), name='article_detail'),
    path('articles/create/', ArticleCreate.as_view(), name='article_create'),
    path('articles/<int:pk>/edit/', ArticleUpdate.as_view(), name='article_edit'),
    path('articles/<int:pk>/delete/', ArticleDelete.as_view(), name='article_delete'),

    path('create/', NewsCreate.as_view(), name='news_create'),
    path('<int:pk>/edit/', NewsUpdate.as_view(), name='news_edit'),
    path('<int:pk>/delete/', NewsDelete.as_view(), name='news_delete'),

    path('category/<int:category_id>/subscribe/', subscribe, name='subscribe'),
    path('category/<int:category_id>/unsubscribe/', unsubscribe, name='unsubscribe'),

    path('test-celery/', TestCeleryView.as_view(), name='test_celery'),
]