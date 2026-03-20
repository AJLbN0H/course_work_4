from celery import shared_task
from mailings.models import Newsletter
from mailings.services import NewsletterService

@shared_task
def send_all_newsletters():
    """
    Периодическая задача, которая проверяет все активные рассылки
    и вызывает сервис отправки почты.
    """
    
    newsletters = Newsletter.objects.exclude(status="Завершена").filter(newsletter_is_disabled=False)
    for newsletter in newsletters:
        NewsletterService.send_newsletter_emails(newsletter.id)
