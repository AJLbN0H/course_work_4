from django.db import models

class MailingRecipient(models.Model): #Получатель рассылки

    email = models.CharField(unique=True, max_length=150, verbose_name="Email", help_text="Введите ваш email")
    full_name = models.CharField(max_length=150, verbose_name="Ф.И.О", help_text="Введите ваше Ф.И.О")
    comment = models.TextField(verbose_name="Комментарий", help_text="Напишите свой комментарий")

    def __str__(self):
        return f'{self.full_name}, {self.email}'

    class Meta:
        verbose_name = "Клиент"
        verbose_name_plural = "Клиенты"
        ordering = ["email", 'full_name']


class Message(models.Model): #Сообщение

    topic = models.CharField(max_length=150, verbose_name="Тема письма", help_text="Введите тему письма")
    content = models.TextField(verbose_name="Тело письма", help_text="Напишите содержание письма")

    def __str__(self):
        return f'{self.topic}'

    class Meta:
        verbose_name = "Сообщение"
        verbose_name_plural = "Сообщения"
        ordering = ["topic"]


class Newsletter(models.Model): #Рассылки

    sending_date = models.DateTimeField(verbose_name="Дата и время первой отправки")
    end_date_of_send = models.DateTimeField(verbose_name="Дата и время окончания отправки")
    status = models.CharField(max_length=9, verbose_name="Статус")
    message  = models.ForeignKey(Message, verbose_name="Сообщение", blank=True, null=True, on_delete=models.CASCADE)
    recipients = models.ManyToManyField(MailingRecipient, verbose_name="Получатели", blank=True, null=True)

    def __str__(self):
        return f'{self.status}, {self.message}, {self.recipients}'

    class Meta:
        verbose_name = "Рассылка"
        verbose_name_plural = "Рассылки"
        ordering = ["sending_date", "end_date_of_send", "status"]


class AttemptToSend(models.Model): #Попытка рассылки

    date_of_attempt = models.DateTimeField(verbose_name="Дата и время попытки", auto_now=True)
    status = models.CharField(max_length=10, verbose_name="Статус")
    mail_server_response = models.TextField(verbose_name="Ответ почтового сервера")
    newsletter  = models.ForeignKey(Newsletter, verbose_name="Рассылка", blank=True, null=True, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.status}, {self.date_of_attempt}'

    class Meta:
        verbose_name = "Попытка рассылки"
        verbose_name_plural = "Попытки рассылок"
        ordering = ["date_of_attempt", "status"]
