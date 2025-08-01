from django.conf import settings
from django.core.mail import send_mail
from django.shortcuts import reverse
from django.views.generic import TemplateView, FormView

from fitnessApp.forms import ContactUsForm

class ContactUsSuccessView(TemplateView):
    template_name = "pages/contactus_success.html"

class SupportView(FormView):
    form_class = ContactUsForm
    template_name = "pages/support.html"

    def get_success_url(self):
        return reverse("pages-contactus-success")

    def form_valid(self, form):
        email = form.cleaned_data.get("email")
        subject = form.cleaned_data.get("subject")
        message = form.cleaned_data.get("message")

        full_message = f"""Received message below:\n\nEmail: {email} \nSubject: {subject}\n___________________________________\n\n{message}"""
        send_mail(subject="Received contact us form: " + subject,
                  message=full_message,
                  from_email=settings.DEFAULT_FROM_EMAIL,
                  recipient_list=[settings.DEFAULT_FROM_EMAIL],)
        
        return super(SupportView, self).form_valid(form)