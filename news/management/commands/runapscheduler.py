import logging

from django.conf import settings

from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.triggers.cron import CronTrigger
from django.core.management.base import BaseCommand
from django_apscheduler.jobstores import DjangoJobStore
from django_apscheduler.models import DjangoJobExecution

logger = logging.getLogger(__name__)

def weekly_newsletter():
    from datetime import datetime, timedelta
    from django.core.mail import EmailMultiAlternatives
    from django.template.loader import render_to_string
    from news.models import Category, Post

    week_ago = datetime.now() - timedelta(days=7)
    new_posts = Post.objects.filter(created_at__gte=week_ago, post_type='AR')

    for category in Category.objects.all():
        posts_in_cat = new_posts.filter(categories=category)
        if not posts_in_cat.exists():
            continue

        subscribers = category.subscribers.all()
        if not subscribers.exists():
            continue

        html_content = render_to_string(
            'email/weekly_news.html',
            {
                'category': category.name,
                'posts': posts_in_cat,
            }
        )

        msg = EmailMultiAlternatives(
            subject=f'новые статьи в категории {category.name}',
            body='',
            from_email=settings.DEFAULT_FROM_EMAIL,
            to=[user.email for user in subscribers]
        )
        msg.attach_alternative(html_content, "text/html")
        msg.send()

def delete_old_job_executions(max_age=604_800):
    DjangoJobExecution.objects.delete_old_job_executions(max_age)

class Command(BaseCommand):
    help = "Runs apscheduler."

    def handle(self, *args, **options):
        scheduler = BlockingScheduler(timezone=settings.TIME_ZONE)
        scheduler.add_jobstore(DjangoJobStore(), "default")

        scheduler.add_job(
            weekly_newsletter,
            trigger=CronTrigger(day_of_week="mon", hour=8, minute=0),
            id="weekly_newsletter",
            max_instances=1,
            replace_existing=True,
        )
        logger.info("добавлена задача weekly_newsletter")

        scheduler.add_job(
            delete_old_job_executions,
            trigger=CronTrigger(day_of_week="mon", hour="00", minute="00"),
            id="delete_old_job_executions",
            max_instances=1,
            replace_existing=True,
        )
        logger.info("добавлена задача delete_old_job_executions")

        try:
            logger.info("запуск планировщика...")
            scheduler.start()
        except KeyboardInterrupt:
            logger.info("остановка планировщика...")
            scheduler.shutdown()
            logger.info("планировщик остановлен")