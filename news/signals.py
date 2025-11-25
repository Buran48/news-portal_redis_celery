from django.db.models.signals import m2m_changed
from django.dispatch import receiver
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from .models import Post
from .templatetags.custom_filters import censor


@receiver(m2m_changed, sender=Post.categories.through)
def notify_subscribers(sender, instance, action, **kwargs):
    if action == "post_add":
        subscribers_data = {}
        for category in instance.categories.all():
            for subscriber in category.subscribers.all():
                if subscriber.email and subscriber.email not in subscribers_data:
                    subscribers_data[subscriber.email] = {
                        'username': subscriber.username,
                        'email': subscriber.email
                    }

        for email, subscriber_info in subscribers_data.items():
            html_content = render_to_string(
                'email/new_post_notification.html',
                {
                    'post': instance,
                    'username': subscriber_info['username'],
                }
            )

            censored_title = censor(instance.title)

            msg = EmailMultiAlternatives(
                subject=censored_title,
                body=f'Здравствуй, {subscriber_info["username"]}. Новая {"новость" if instance.post_type == "NW" else "статья"} на портале',
                from_email='newsporta1700@gmail.com',
                to=[email],
            )
            msg.attach_alternative(html_content, "text/html")
            msg.send()