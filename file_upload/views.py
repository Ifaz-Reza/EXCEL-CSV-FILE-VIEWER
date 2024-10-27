import pandas as pd
from django.shortcuts import render, redirect
from django.core.mail import send_mail
from django.conf import settings
from .forms import UploadFileForm

def file_upload_view(request):
    if request.method == "POST":
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            file = request.FILES["file"]
            summary = generate_summary(file)
            send_summary_email(summary)  # Email the summary
            return render(request, "file_upload/success.html", {"summary": summary})
    else:
        form = UploadFileForm()
    return render(request, "file_upload/upload.html", {"form": form})

def generate_summary(file):
    df = pd.read_csv(file) if file.name.endswith(".csv") else pd.read_excel(file)
    summary = df.describe().to_string()
    return summary

def send_summary_email(summary):
    subject = "Python Assignment - Your Name"
    message = summary
    recipient_list = ["tech@themedius.ai"]
    try:
        send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, recipient_list)
        print("Email sent successfully!")
    except Exception as e:
        print(f"Error sending email: {e}")



