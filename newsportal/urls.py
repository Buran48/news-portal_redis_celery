from django.contrib import admin
from django.urls import path, include
from django.views.generic import RedirectView
from news.views import ArticlesList, ArticleDetail, ArticleCreate, ArticleUpdate, ArticleDelete

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', RedirectView.as_view(url='/news/')),
    path('news/', include('news.urls')),
    path('articles/', ArticlesList.as_view(), name='articles_list_root'),
    path('articles/<int:pk>/', ArticleDetail.as_view(), name='article_detail_root'),
    path('articles/create/', ArticleCreate.as_view(), name='article_create_root'),
    path('articles/<int:pk>/edit/', ArticleUpdate.as_view(), name='article_edit_root'),
    path('articles/<int:pk>/delete/', ArticleDelete.as_view(), name='article_delete_root'),
    path('accounts/', include('accounts.urls')),
    path('accounts/', include('allauth.urls')),
    path('protect/', include('protect.urls')),
]