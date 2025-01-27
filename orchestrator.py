import os
import subprocess
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
from email.mime.text import MIMEText
from datetime import datetime

VENV_PATH = os.path.join(os.path.dirname(__file__), "venv")
SCRAPER_FOLDER = os.path.dirname(__file__)

def get_activate_command():
    """Get the correct command to activate the virtual environment based on OS."""
    if os.name == "nt":  # Windows
        return os.path.join(VENV_PATH, "Scripts", "activate")
    else:  # Unix/Linux/Mac
        return f"source {os.path.join(VENV_PATH, 'bin', 'activate')}"

def run_scraper(script_name):
    """Run a scraper script within the virtual environment."""
    script_path = os.path.join(SCRAPER_FOLDER, script_name)

    activate_command = get_activate_command()

    command = f"bash -c '{activate_command} && python {script_path}'"
    print(f"Running {script_name}...")

    result = subprocess.run(command, shell=True, capture_output=True, text=True)

    if result.returncode == 0:
        print(f"{script_name} ran successfully.")
    else:
        print(f"Error running {script_name}:")
        print(result.stderr)

def send_email_with_attachment(to_email, subject, body, attachment_path):
    """Send an email with the attachment."""
    from_email = os.getenv("GMAIL_USER")  # Get email from environment variable
    password = os.getenv("GMAIL_PASSWORD")  # Get password from environment variable

    msg = MIMEMultipart()
    msg['From'] = from_email
    msg['To'] = to_email
    msg['Subject'] = subject

    msg.attach(MIMEText(body, 'plain'))

    with open(attachment_path, "rb") as attachment:
        part = MIMEBase('application', 'octet-stream')
        part.set_payload(attachment.read())
        encoders.encode_base64(part)
        part.add_header('Content-Disposition', f"attachment; filename={attachment_path}")
        msg.attach(part)

    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(from_email, password)
        text = msg.as_string()
        server.sendmail(from_email, to_email, text)
        server.quit()
        print(f"Email successfully sent to {to_email}")
    except Exception as e:
        print(f"Failed to send email: {e}")

def main():
    scrapers = [
        "scrape_olimpica.py"
    ]

    for scraper in scrapers:
        run_scraper(scraper)

    current_date = datetime.now().strftime("%Y-%m-%d")
    output_file = f"olimpica_products_{current_date}.xlsx"

    send_email_with_attachment(
        to_email=os.getenv("RECIPIENT_EMAIL"),
        subject="Olimpica Scraped Data",
        body="Please find attached the scraped data from Olimpica.",
        attachment_path=output_file
    )

if __name__ == "__main__":
    main()