from django_filters import FilterSet, DateFilter, CharFilter
from django import forms
from .models import Post


class PostFilter(FilterSet):
    title = CharFilter(
        field_name='title',
        lookup_expr='icontains',
        label='есть  в названии'
    )

    author = CharFilter(
        field_name='author__user__username',
        lookup_expr='icontains',
        label='есть  в имени автора'
    )

    created_after = DateFilter(
        field_name='created_at',
        lookup_expr='gt',
        label='после даты',
        widget=forms.DateInput(attrs={'type': 'date'})
    )

    class Meta:
        model = Post
        fields = {
            'title': ['icontains'],
            'created_at': ['gt'],
        }