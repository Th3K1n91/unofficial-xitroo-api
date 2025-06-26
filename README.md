# Unofficial Xitroo API for Python

[![PyPI version](https://img.shields.io/pypi/v/unofficial-xitroo-api.svg)](https://pypi.org/project/unofficial-xitroo-api/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python Version](https://img.shields.io/pypi/pyversions/unofficial-xitroo-api.svg)](https://pypi.org/project/unofficial-xitroo-api/)

A powerful and easy-to-use Python wrapper for the [Xitroo](https://xitroo.com) temporary email service. This library allows you to programmatically create temporary email addresses, read inboxes, parse emails, handle attachments, and even send emails.

- **Author:** [Th3K1n91](https://github.com/Th3K1n91)
- **Source Code:** [https://github.com/Th3K1n91/unofficial-xitroo-api](https://github.com/Th3K1n91/unofficial-xitroo-api)

## ✨ Key Features

- **📧 Generate Email Addresses:** Instantly create random Xitroo email addresses.
- **📥 Full Inbox Control:** Fetch all emails from an inbox, get the total count, and access individual emails.
- **📖 Read Emails:** Parse email content, including subject, sender, HTML body, and plain text body.
- **🔢 Automatic Code Parsing:** Easily extract verification codes (e.g., `123456`) from email bodies.
- **🔎 Powerful Search:** Search your inbox by sender, subject, date, or specific text within the email body.
- **📎 Attachment Handling:** List, download, or read attachments directly.
- **📤 Send Emails:** Send emails from your temporary address (with CAPTCHA handling).
- **🗑️ Delete Emails:** Clean up your inbox by deleting unwanted emails.
- **⏱️ Wait for New Mail:** Asynchronously wait for the latest email to arrive.

## 📦 Installation

Install the library using `pip`:

```bash
pip install unofficial-xitroo-api
```

This library depends on the `requests` package, which will be installed automatically.

## 🚀 Usage Examples

Here are some common use cases to get you started.

### Quick Start: Get a New Email and Read It

This example generates a new random email address, waits for the first email to arrive, and prints its subject and body.

```python
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

```

### Reading an Inbox

You can easily access an inbox and iterate through all the emails it contains.

```python
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
```

### Searching the Inbox

The `searchInbox` method provides a flexible way to find specific emails without iterating through the entire inbox yourself.

```python
from xitroo import Xitroo

client = Xitroo("example@xitroo.de")
search = client.searchInbox()

# Search for all emails from "support@company.com"
print("Searching for emails from 'support@company.com'...")
results_by_sender = search.BY.SENDER("support@company.com")
print(f"Found {len(results_by_sender)} emails.")
for mail in results_by_sender:
    print(f"  - ID: {mail.getId()}, Subject: {mail.getSubject()}")


# Search for all emails with "verification" in the title
print("\nSearching for emails with 'Verification' in the subject...")
results_by_title = search.BY.TITLE("Verification")
print(f"Found {len(results_by_title)} emails.")
for mail in results_by_title:
    print(f"  - ID: {mail.getId()}, Subject: {mail.getSubject()}")
```

### Sending an Email (with CAPTCHA)

You can send emails programmatically. This requires solving a CAPTCHA. The library supports both manual and programmatic solving.

**Mode 1: Manual CAPTCHA Solving (User Input)**
The library will print the CAPTCHA to the console and wait for you to type the solution.

```python
from xitroo import Xitroo

# Use your generated email address as the sender
sender_client = Xitroo(Xitroo.generate())

print(f"Sending email from: {sender_client.getMailAddress()}")

# Use mode=1 for manual input
# The CAPTCHA image text will be printed to the console
success = sender_client.sendMail(
    recipient="test-recipient@example.com",
    subject="Hello from Xitroo API!",
    Text="This is a test email sent using the Python library.",
    mode=1 
)

if success:
    print("Email sent successfully!")
else:
    print("Failed to send email.")
```

**Mode 0: Programmatic CAPTCHA Solving**
If you have an external CAPTCHA solving service, you can get the CAPTCHA data and submit the solution yourself.

```python
from xitroo import Xitroo

client = Xitroo("your-email@xitroo.com")

# 1. Get the captcha object
captcha_handler = client.Captcha()

# 2. Get captcha data
captcha_data = captcha_handler.getCaptcha()
captcha_id = captcha_data["authID"]
captcha_image_code = captcha_data["captchaCode"] # This is the base64 encoded image

# --- Here you would send captcha_image_code to your solving service ---
# --- For this example, we'll pretend the solution is 'ABCDE' ---
solution = "ABCDE" # Replace with the actual solution

# 3. Verify the solution to get an auth token
if captcha_handler.verifyCaptcha(solution):
    print("Captcha solved! Sending email...")
    # 4. Use the captcha_id to send the mail with mode=0
    success = client.sendMail(
        recipient="test@example.com",
        subject="Automated Email",
        Text="This was sent programmatically.",
        mode=0,
        id=captcha_id
    )
    if success:
        print("Email sent!")
    else:
        print("Email sending failed.")
else:
    print("Captcha verification failed.")
```

### Handling Attachments

Download or read attachments from an email.

```python
from xitroo import Xitroo

client = Xitroo("your-email@xitroo.com")
inbox = client.Inbox()

if len(inbox) > 0:
    # Get the latest mail
    mail = inbox.getMailFirst()
    
    # List attachments
    attachments = mail.getAttachments()
    if attachments:
        print(f"Found {len(attachments)} attachments.")
        for attachment in attachments:
            filename = attachment['filename']
            print(f" - Attachment Filename: {filename}")
            
            # Download the attachment
            success = mail.downloadAttachment(filename, path=".") # Download to current directory
            if success:
                print(f"   '{filename}' downloaded successfully.")
            else:
                print(f"   Failed to download '{filename}'.")
    else:
        print("No attachments found in the latest email.")
```

---

## API Documentation

### `Xitroo` Class

This is the main class to interact with the API.

- `Xitroo(mailAddress, header={}, session=None)`: Constructor.
  - `mailAddress` (str): The full Xitroo email address (e.g., `user@xitroo.de`).
- `generate(prefix="", suffix="", locale="de", randomletterscount=10)` (staticmethod): Generates a random email address string.
- `getCode(body, codelength=6)` (staticmethod): Extracts a numerical code of a given length from a string.
- `getMailAddress()`: Returns the current mail address.
- `setMailAddress(mailAddress)`: Changes the mail address for the instance.
- `Inbox()`: Returns an `Inbox` object for the current mail address.
- `Mail(mailId)`: Returns a `Mail` object for a specific mail ID.
- `getLatestMail()`: Returns a `Mail` object for the most recent email, or `None`.
- `waitForLatestMail(maxTime=60, sleepTime=5, checkMail=100)`: Waits for a new email to arrive and returns it.
- `sendMail(recipient, subject, Text, mode=1, id="")`: Sends an email.
  - `mode=1`: Manual user input for CAPTCHA.
  - `mode=0`: Programmatic; requires a valid `id` from a solved `Captcha`.
- `searchInbox()`: Returns a `SearchMail` object to perform searches.
- `Captcha()`: Returns a `Captcha` object for handling CAPTCHAs.

### `Inbox` Class

Represents the email inbox. Accessed via `Xitroo.Inbox()`.

- `__len__()`: Returns the total number of emails in the inbox.
- `__getitem__(index)`: Allows iteration (e.g., `for mail in inbox:`). Returns a `Mail` object.
- `getMail(index)`: Returns a `Mail` object at a specific index.
- `getMailFirst()`: Returns the newest email in the inbox.
- `getMailLast()`: Returns the oldest email in the inbox.
- `getRawInbox()`: Returns the raw JSON response from the API for the inbox.

### `Mail` Class

Represents a single email. Accessed from an `Inbox` object or `Xitroo.Mail(id)`.

- `getId()`: Returns the mail's unique ID.
- `getSubject()`: Returns the email subject as a decoded string.
- `getBodyHtml()`: Returns the full HTML body of the email.
- `getBodyText()`: Returns the plain text body of the email.
- `getFromMail()`: Returns the sender's email address.
- `getArrivalTimestamp()`: Returns the arrival timestamp.
- `getCode(codelength=6)`: Searches the text body for a numerical code of `codelength` and returns it as a string.
- `getAttachments()`: Returns a list of attachment dictionaries.
- `downloadAttachment(filetodownload, path=None)`: Downloads a named attachment to a specified path.
- `readAttachment(filetoread, encoding='utf-8')`: Reads a named attachment and returns its content as a string.
- `delete()`: Deletes the email from the inbox.
- `getRawMail()`: Returns the raw JSON response for the email.

### `SearchMail` Class

Provides methods for searching. Accessed via `Xitroo.searchInbox()`.

- **Usage:**
  ```python
  search = client.searchInbox()
  results = search.BY.METHOD(query)
  ```
- **`search.BY` Methods:**
  - `SENDER(sender_str)`: Search for emails where the sender contains `sender_str`.
  - `TITLE(title_str)`: Search for emails where the subject contains `title_str`.
  - `TEXT(text_str)`: Search for emails where the body contains `text_str`.
  - `DATE(datetime_obj)`: Search for emails that arrived on the same date as the `datetime` object.
- Each search method returns a new `Inbox` object containing only the search results.

### `Captcha` Class

Handles CAPTCHA generation and verification. Accessed via `Xitroo.Captcha()`.

- `getCaptcha()`: Requests a new CAPTCHA from the server. Returns a `dict` containing the `authID` and the base64-encoded `captchaCode` (image).
- `verifyCaptcha(solution, captchaid="")`: Submits a solution for a given CAPTCHA ID. Returns `True` on success, `False` on failure.