from xitroo import Xitroo

# 1. Generate a random email address
random_email = Xitroo.generate()
print(f"Using temporary email: {random_email}")

# 2. Create a Xitroo instance
client = Xitroo(random_email)

# 3. Wait for the latest email to arrive (up to 60 seconds)
print("Waiting for a new email...")
# The waitForLatestMail method is ideal for automation scripts
latest_mail = client.waitForLatestMail()

if latest_mail:
    print("\n--- New Email Received! ---")
    print(f"From: {latest_mail.getFromMail()}")
    print(f"Subject: {latest_mail.getSubject()}")

    # Get a verification code from the email body
    try:
        code = latest_mail.getCode()
        print(f"Verification Code: {code}")
    except AttributeError:
        print("No verification code found in the email.")

    print("\n--- Email Body (Text) ---")
    print(latest_mail.getBodyText())
else:
    print("No email received within the time limit.")