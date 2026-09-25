import requests
import smtplib
import os
from email.message import EmailMessage
from datetime import datetime, timedelta

# Zieltag bestimmen
heute = datetime.now()

if heute.weekday() == 4:  # Freitag -> Montag
    zieltag = heute + timedelta(days=3)
elif heute.weekday() == 5:  # Samstag -> Montag
    zieltag = heute + timedelta(days=2)
else:  # alle anderen Tage -> nächster Tag
    zieltag = heute + timedelta(days=1)

datum = zieltag.strftime("%d-%m-%Y")

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

# E-Mail erstellen
mail = EmailMessage()

mail["Subject"] = f"Vertretungsplan {datum}"
mail["From"] = os.getenv("MAIL_USER")
mail["To"] = "bastian_bruenner@t-online.de"

mail.set_content(
    f"""Der aktuelle Vertretungsplan ist verfügbar:

{
