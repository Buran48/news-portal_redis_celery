from django.views.generic import ListView, DetailView
from django.views.generic import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.mixins import PermissionRequiredMixin
from .models import Post
from .filters import PostFilter
from .forms import PostForm
from django.utils import timezone
from django.conf import settings


class BasePostList(ListView):
    template_name = 'news.html'
    context_object_name = 'posts'
    paginate_by = 10
    post_type = None

    def get_queryset(self):
        queryset = Post.objects.filter(post_type=self.post_type).order_by('-created_at')
        self.filterset = PostFilter(self.request.GET, queryset)
        return self.filterset.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filterset'] = self.filterset
        return context


class NewsList(BasePostList):
    post_type = 'NW'


class ArticlesList(BasePostList):
    post_type = 'AR'


class NewsDetail(DetailView):
    model = Post
    template_name = 'one_news.html'
    context_object_name = 'one_news'


class ArticleDetail(DetailView):
    model = Post
    template_name = 'one_article.html'
    context_object_name = 'one_article'


class NewsCreate(PermissionRequiredMixin, LoginRequiredMixin, CreateView):
    permission_required = ('news.add_post',)
    form_class = PostForm
    model = Post
    template_name = 'post_edit.html'

    def form_valid(self, form):
        user = self.request.user
        today = timezone.now().date()
        posts_today = Post.objects.filter(author__user=user, post_type='NW', created_at__date=today).count()

        if posts_today >= settings.MAX_NEWS_PER_DAY:
            form.add_error(None, f'нельзя публиковать более {settings.MAX_NEWS_PER_DAY} новостей в сутки')
            return self.form_invalid(form)

        post = form.save(commit=False)
        post.post_type = 'NW'
        post.save()
        form.save_m2m()

        return super().form_valid(form)


class ArticleCreate(PermissionRequiredMixin, LoginRequiredMixin, CreateView):
    permission_required = ('news.add_post',)
    form_class = PostForm
    model = Post
    template_name = 'post_edit.html'

    def form_valid(self, form):
        post = form.save(commit=False)
        post.post_type = 'AR'
        post.save()
        form.save_m2m()

        return super().form_valid(form)


class NewsUpdate(PermissionRequiredMixin, LoginRequiredMixin, UpdateView):
    form_class = PostForm
    model = Post
    template_name = 'post_edit.html'


class ArticleUpdate(PermissionRequiredMixin, LoginRequiredMixin, UpdateView):
    form_class = PostForm
    model = Post
    template_name = 'post_edit.html'


class NewsDelete(PermissionRequiredMixin, LoginRequiredMixin, DeleteView):
    permission_required = ('news.delete_post',)
    model = Post
    template_name = 'post_delete.html'
    success_url = reverse_lazy('news_list')


class ArticleDelete(PermissionRequiredMixin, LoginRequiredMixin, DeleteView):
    permission_required = ('news.delete_post',)
    model = Post
    template_name = 'post_delete.html'
    success_url = reverse_lazy('articles_list')


class NewsSearch(BasePostList):
    template_name = 'news_search.html'
    post_type = 'NW'


from django.shortcuts import redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Category, CategorySubscriber


@login_required
def subscribe(request, category_id):
    category = get_object_or_404(Category, id=category_id)
    CategorySubscriber.objects.get_or_create(category=category, user=request.user)
    return redirect('news_list')


@login_required
def unsubscribe(request, category_id):
    category = get_object_or_404(Category, id=category_id)
    CategorySubscriber.objects.filter(category=category, user=request.user).delete()
    return redirect('news_list')