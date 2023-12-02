import smtplib
import imaplib
import email
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication

# Email configuration for Gmail
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587
SMTP_USERNAME = "yourusername@gmail.com"
SMTP_PASSWORD = "yourpassword"

IMAP_SERVER = "imap.gmail.com"
IMAP_PORT = 993
IMAP_USERNAME = "yourusername@gmail.com"
IMAP_PASSWORD = "yourpassword"


def send_email(to_email, subject, message, attachments=[]):
    # Create an SMTP connection
    smtp_server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
    smtp_server.starttls()
    smtp_server.login(SMTP_USERNAME, SMTP_PASSWORD)

    # Create the email message
    msg = MIMEMultipart()
    msg["From"] = SMTP_USERNAME
    msg["To"] = to_email
    msg["Subject"] = subject

    # Attach the message body
    msg.attach(MIMEText(message, "plain"))

    # Attach any files
    for attachment in attachments:
        with open(attachment, "rb") as file:
            part = MIMEApplication(file.read(), Name=attachment)
            breakpoint()
            part["Content-Disposition"] = f'attachment; filename="{attachment}"'
            msg.attach(part)

    # Send the email
    smtp_server.sendmail(SMTP_USERNAME, to_email, msg.as_string())

    # Close the SMTP connection
    smtp_server.quit()


def receive_emails():
    # Create an IMAP connection
    imap_server = imaplib.IMAP4_SSL(IMAP_SERVER, IMAP_PORT)
    imap_server.login(IMAP_USERNAME, IMAP_PASSWORD)
    imap_server.select("inbox")

    # Search for all emails in the inbox
    _, email_data = imap_server.search(None, "ALL")
    email_ids = email_data[0].split()

    # Retrieve and print email messages
    for email_id in email_ids:
        _, msg_data = imap_server.fetch(email_id, "(RFC822)")
        msg = email.message_from_bytes(msg_data[0][1])
        print(f"Subject: {msg['Subject']}")
        print(f"From: {msg['From']}")
        print(f"Date: {msg['Date']}")
        print(f"Message:\n{msg.get_payload(decode=True).decode('utf-8')}")

    # Close the IMAP connection
    imap_server.logout()


if __name__ == "__main__":
    # Send an email with attachments
    attachments = [
        "/home/dino/Documents/python-projects/catleaves.txt",
        "/home/dino/Documents/python-projects/color_codes.txt",
    ]  # Replace with your attachment filenames
    send_email(
        "receiversemail@gmail.com",
        "subject name here",
        "This is a test email with attachments.",
        attachments,
    )

    # Receive and print emails
    breakpoint()
    receive_emails()
