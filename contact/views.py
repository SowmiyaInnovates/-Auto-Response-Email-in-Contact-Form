import openai
from django.conf import settings
from django.core.mail import send_mail
from django.http import HttpResponse
from django.shortcuts import render
from .forms import ContactForm

openai.api_key = settings.OPENAI_API_KEY


import openai

def generate_auto_reply(message):
    openai.api_key = 'ur-open-api-key'

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",  # Or any other model available
        messages=[
            {"role": "user", "content": message}
        ]
    )
    return response.choices[0].message['content']


def contact_view(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            # Get the form data
            name = form.cleaned_data['name']
            email = form.cleaned_data['email']
            message = form.cleaned_data['message']

            # Generate auto-reply using OpenAI
            auto_reply = generate_auto_reply(message)

            # Send auto-reply email
            send_mail(
                'Re: Your Contact Form Submission',
                auto_reply,
                'your_email@example.com',
                [email],
                fail_silently=False,
            )

            return HttpResponse('Thank you for your message. An auto-reply has been sent to your email.')

    else:
        form = ContactForm()

    return render(request, 'contact.html', {'form': form})
