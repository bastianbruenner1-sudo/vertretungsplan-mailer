import requests
import smtplib
import os
from email.message import EmailMessage
from datetime import datetime, timedelta

# Datum für morgen
morgen = datetime.now()
datum = morgen.strftime("%d-%m-%Y")

# Dateiname
pdf_name = f"vertretungen-{datum}.pdf"

# URL zur PDF
url = f"https://100017.fuxnoten.com/uploads/lessondata/{pdf_name}"

# PDF herunterladen
r = requests.get(url)

if r.status_code != 200:
    print("Keine PDF vorhanden.")
    quit()

# PDF speichern
with open(pdf_name, "wb") as f:
    f.write(r.content)

print(f"PDF gespeichert: {pdf_name}")

# GitHub-Pages-Link
github_link = (
    f"https://bastianbruenner1-sudo.github.io/"
    f"vertretungsplan-mailer/{pdf_name}"
)

# Mail erstellen
mail = EmailMessage()

mail["Subject"] = f"Vertretungsplan {datum}"
mail["From"] = os.getenv("MAIL_USER")
mail["To"] = "bastian_bruenner@t-online.de"

mail.set_content(
    f"""Der aktuelle Vertretungsplan ist verfügbar:

{github_link}

Diese Mail wurde automatisch erstellt.
"""
)

# Mail versenden
with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
    smtp.login(
        os.getenv("MAIL_USER"),
        os.getenv("MAIL_PASS")
    )
    smtp.send_message(mail)

print("Mail versendet")
