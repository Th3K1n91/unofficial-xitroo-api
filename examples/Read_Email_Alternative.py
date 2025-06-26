from xitroo import Xitroo, EmailNotFound

# Use an existing email address
client = Xitroo("example@xitroo.de")

try:
    # Get the Inbox object
    inbox = client.Inbox()

    print(f"Total emails in inbox: {len(inbox)}")

    # Iterate through all emails
    for mail in inbox:
        print(f" - Subject: {mail.getSubject()}")

    # Get the first and last emails
    if len(inbox) > 0:
        first_mail = inbox.getMailFirst()
        print(f"\nOldest email subject: {first_mail.getSubject()}")

        last_mail = inbox.getMailLast()
        print(f"Newest email subject: {last_mail.getSubject()}")

except EmailNotFound as e:
    print(e)