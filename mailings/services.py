from django.utils import timezone
from django.core.mail import send_mail
from django.conf import settings
from mailings.models import Newsletter, AttemptToSend


class NewsletterService:

    @staticmethod
    def send_newsletter_emails(newsletter_id):

        newsletter = Newsletter.objects.get(id=newsletter_id)

        if (
            newsletter.sending_date <= timezone.now()
            or newsletter.sending_date == timezone.now()
        ):

            if (
                not newsletter.end_date_of_send <= timezone.now()
                or newsletter.end_date_of_send == timezone.now()
            ):

                newsletter.status = "Запущена"

                subject = newsletter.message.topic
                message_ = newsletter.message.content
                from_email = settings.DEFAULT_FROM_EMAIL
                recipient_list = [
                    recipient.email for recipient in newsletter.recipients.all()
                ]
                try:
                    send_mail(subject, message_, from_email, recipient_list)
                except Exception as e:
                    attempt = AttemptToSend(
                        date_of_attempt=timezone.now(),
                        status="Не успешно",
                        mail_server_response=e,
                        newsletter=newsletter,
                    )
                    attempt.save()
                else:
                    attempt = AttemptToSend(
                        date_of_attempt=timezone.now(),
                        status="Успешно",
                        mail_server_response="Сообщение отправлено",
                        newsletter=newsletter,
                    )
                    attempt.save()

                newsletter.save()

        if (
            newsletter.end_date_of_send <= timezone.now()
            or newsletter.end_date_of_send == timezone.now()
        ):

            newsletter.status = "Завершена"
            newsletter.save()
