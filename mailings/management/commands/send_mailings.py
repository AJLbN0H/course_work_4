from django.conf import settings
from django.core.mail import send_mail
from django.core.management import BaseCommand


class Command(BaseCommand):
    help = "Отправка рассылки вручную через командную строку"

    def handle(self, *args, **options):

        subject = "Рассылка вручную"
        message = "Вы отправили это сообщение через кастомную команду"
        from_email = settings.DEFAULT_FROM_EMAIL
        recipient_list = [input("Введите ваш email(Yandex): ")]
        send_mail(subject, message, from_email, recipient_list)
