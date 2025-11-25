from celery import shared_task
import time
from datetime import datetime, timedelta
from .models import Post, Category
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.conf import settings


@shared_task
def hello():
    time.sleep(10)
    print("Hello, world!")


@shared_task
def weekly_newsletter():
    week_ago = datetime.now() - timedelta(days=7)
    recent_posts = Post.objects.filter(created_at__gte=week_ago, post_type='AR')

    for category in Category.objects.all():
        posts_in_category = recent_posts.filter(categories=category)
        if not posts_in_category.exists():
            continue

        subscribers = category.subscribers.all()
        if not subscribers.exists():
            continue

        for subscriber in subscribers:
            if subscriber.email:
                html_content = render_to_string(
                    'email/weekly_news.html',
                    {
                        'category': category.name,
                        'posts': posts_in_category,
                        'username': subscriber.username,
                    }
                )

                msg = EmailMultiAlternatives(
                    subject=f'Новые статьи в категории {category.name}',
                    body='',
                    from_email=settings.DEFAULT_FROM_EMAIL,
                    to=[subscriber.email],
                )
                msg.attach_alternative(html_content, "text/html")
                msg.send()