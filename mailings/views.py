from django.core.cache import cache
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from django.views.generic import (
    CreateView,
    ListView,
    UpdateView,
    DeleteView,
    DetailView,
)

from mailings.forms import (
    MessageForm,
    MailingRecipientForm,
    NewsletterForm,
    NewsletterIsDisabledForm,
)
from mailings.models import Message, MailingRecipient, Newsletter, AttemptToSend
from mailings.services import NewsletterService


class MessageListView(ListView):
    model = Message
    context_object_name = "messages"
    template_name = "mailings_message/message_list.html"

    def get_queryset(self):
        queryset = cache.get("message_list_view")
        if not queryset:
            queryset = super().get_queryset()
            cache.set("message_list_view", queryset, 60 * 15)


@method_decorator(cache_page(60 * 15), name="dispatch")
class MessageDetailView(DetailView):
    model = Message
    context_object_name = "message"
    template_name = "mailings_message/message_detail.html"


class MessageCreateView(CreateView):
    model = Message
    form_class = MessageForm
    success_url = reverse_lazy("mailings:message_list")
    template_name = "mailings_message/message_create.html"

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


class MessageUpdateView(UpdateView):
    model = Message
    form_class = MessageForm
    success_url = reverse_lazy("mailings:message_list")
    template_name = "mailings_message/message_update.html"


class MessageDeleteView(DeleteView):
    model = Message
    success_url = reverse_lazy("mailings:message_list")
    template_name = "mailings_message/message_delete.html"


class MailingRecipientListView(ListView):
    model = MailingRecipient
    context_object_name = "mailing_recipients"
    template_name = "mailings_mailing_recipient/mailing_recipient_list.html"

    def get_queryset(self):
        queryset = cache.get("mailing_recipient_list")
        if not queryset:
            queryset = super().get_queryset()
            cache.set("mailing_recipient_list", queryset, 60 * 15)


@method_decorator(cache_page(60 * 15), name="dispatch")
class MailingRecipientDetailView(DetailView):
    model = MailingRecipient
    context_object_name = "mailing_recipient"
    template_name = "mailings_mailing_recipient/mailing_recipient_detail.html"


class MailingRecipientCreateView(CreateView):
    model = MailingRecipient
    form_class = MailingRecipientForm
    success_url = reverse_lazy("mailings:mailing_recipient_list")
    template_name = "mailings_mailing_recipient/mailing_recipient_create.html"

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)


class MailingRecipientUpdateView(UpdateView):
    model = MailingRecipient
    form_class = MailingRecipientForm
    success_url = reverse_lazy("mailings:mailing_recipient_list")
    template_name = "mailings_mailing_recipient/mailing_recipient_update.html"


class MailingRecipientDeleteView(DeleteView):
    model = MailingRecipient
    success_url = reverse_lazy("mailings:mailing_recipient_list")
    template_name = "mailings_mailing_recipient/mailing_recipient_delete.html"


class NewsletterListView(ListView):
    model = Newsletter
    context_object_name = "newsletters"
    template_name = "mailings_newsletter/newsletter_list.html"

    def get_queryset(self):

        queryset = cache.get("newsletter_list_view")
        if not queryset:
            queryset = super().get_queryset()
            cache.set("newsletter_list_view", queryset, 60 * 15)

        newsletters = super().get_queryset()
        for newsletter in newsletters:
            NewsletterService.send_newsletter_emails(newsletter_id=newsletter.id)
        return newsletters and Newsletter.objects.filter(newsletter_is_disabled=False)


@method_decorator(cache_page(60 * 15), name="dispatch")
class NewsletterDetailView(DetailView):
    model = Newsletter
    context_object_name = "newsletter"
    template_name = "mailings_newsletter/newsletter_detail.html"


class NewsletterCreateView(CreateView):
    model = Newsletter
    form_class = NewsletterForm
    success_url = reverse_lazy("mailings:newsletter_list")
    template_name = "mailings_newsletter/newsletter_create.html"

    def form_valid(self, form):
        form.instance.owner = self.request.user
        form.instance.status = "Создана"
        return super().form_valid(form)


class NewsletterUpdateView(UpdateView):
    model = Newsletter
    form_class = NewsletterForm
    success_url = reverse_lazy("mailings:newsletter_list")
    template_name = "mailings_newsletter/newsletter_update.html"


class NewsletterDeleteView(DeleteView):
    model = Newsletter
    success_url = reverse_lazy("mailings:newsletter_list")
    template_name = "mailings_newsletter/newsletter_delete.html"


class HomePageListView(ListView):
    model = Newsletter
    template_name = "mailings_message/home_page.html"

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)

        context["number_of_mailings"] = len(Newsletter.objects.all())
        context["number_of_active_mailings"] = len(
            [
                newsletter
                for newsletter in Newsletter.objects.all()
                if newsletter.status == "Запущена"
            ]
        )
        context["number_of_recipients"] = len(MailingRecipient.objects.all())

        return context

    def get_queryset(self):
        queryset = cache.get("home_page_list_view")
        if not queryset:
            queryset = super().get_queryset()
            cache.set("home_page_list_view", queryset, 60 * 15)


class AttemptToSendListView(ListView):
    model = AttemptToSend
    template_name = "mailings_message/attempt_to_send.html"
    context_object_name = "information"

    def get_queryset(self):
        queryset = cache.get("attempt_to_send_list_view")
        if not queryset:
            queryset = super().get_queryset()
            cache.set("attempt_to_send_list_view", queryset, 60 * 15)


class NewsletterIsDisabledView(UpdateView):
    model = Newsletter
    form_class = NewsletterIsDisabledForm
    template_name = "mailings_newsletter/newsletter_is_disabled.html"
    success_url = reverse_lazy("mailings:newsletter_list")

    def form_valid(self, form):
        form.instance.status = "Завершена"
        return super().form_valid(form)
