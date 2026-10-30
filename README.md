# Email Automation Tool

A simple, deployment-ready email-sending web application built with Python and Streamlit. It validates input, prepares an email message, connects to an SMTP server, and reports whether the server accepted the message.

## Features

- Recipient, subject, and message form
- Basic email-address validation
- SMTP over SSL (port 465) or STARTTLS (port 587)
- Error handling without exposing passwords
- Credentials supplied through Streamlit Secrets or environment variables
- Simple responsive interface suitable for a student project demo

## Project structure

```text
email_automation_tool/
├── app.py
├── requirements.txt
├── README.md
├── .gitignore
└── .streamlit/
    └── secrets.toml.example
```

## Run locally (Windows)

1. Install Python 3.10 or newer.
2. Open a terminal in this project folder.
3. Create and activate a virtual environment:

   ```powershell
   py -m venv .venv
   .\.venv\Scripts\Activate.ps1
   ```

4. Install dependencies:

   ```powershell
   python -m pip install -r requirements.txt
   ```

5. Configure SMTP credentials as environment variables in the same PowerShell terminal. Example for Gmail:

   ```powershell
   $env:SMTP_HOST="smtp.gmail.com"
   $env:SMTP_PORT="465"
   $env:SMTP_USERNAME="your_email@gmail.com"
   $env:SMTP_PASSWORD="your_email_app_password"
   $env:FROM_EMAIL="your_email@gmail.com"
   ```

   Use a provider-approved app password or OAuth-capable integration where required. Never use or share your normal account password.

6. Start the application:

   ```powershell
   streamlit run app.py
   ```

7. Open the local URL shown in the terminal (usually `http://localhost:8501`).

## Deploy to Streamlit Community Cloud

1. Create a GitHub repository and upload `app.py`, `requirements.txt`, `README.md`, and `.gitignore`. Do **not** upload real credentials or a real `secrets.toml`.
2. Sign in to Streamlit Community Cloud and create an app from that repository.
3. Select `app.py` as the main file.
4. Open the deployed app's **Settings → Secrets** and add:

   ```toml
   SMTP_HOST = "smtp.gmail.com"
   SMTP_PORT = "465"
   SMTP_USERNAME = "your_email@gmail.com"
   SMTP_PASSWORD = "your_email_app_password"
   FROM_EMAIL = "your_email@gmail.com"
   ```

5. Save the secrets and restart/redeploy the app.
6. Send a test email to an address you control.

SMTP access can be blocked or restricted by some hosting providers or email providers. If SMTP does not work on the deployment host, use the provider's supported email API instead.

## Gmail configuration notes

- Enable two-step verification if required by your account.
- Create an App Password if Google makes it available for your account.
- Use the App Password in `SMTP_PASSWORD`, not your normal Google password.
- Google Workspace administrators and some account types may disable App Passwords. In that case, use a supported OAuth/API approach.
- Do not publish your credentials in GitHub, screenshots, logs, or the project report.

## Test checklist

- Empty recipient, subject, and message are rejected.
- Invalid recipient format is rejected.
- Missing SMTP credentials prevent sending.
- Correct configuration can submit a test email.
- Incorrect SMTP settings produce a safe error message.
- Check both Inbox and Spam during delivery tests.

## Important limitations

- This version sends one email per submission; it is not a bulk-mailing or campaign platform.
- It does not store messages, passwords, or a history of sent emails.
- A success message means the configured server accepted the message for processing; it does not guarantee inbox delivery.
- AI/ML features such as email classification or AI-generated replies are future enhancements and are not implemented in this version.
- Send only legitimate emails to recipients who expect or have agreed to receive them.

## References

- Python `smtplib`: https://docs.python.org/3/library/smtplib.html
- Python `email` package: https://docs.python.org/3/library/email.html
- Streamlit documentation: https://docs.streamlit.io/
- Visual Studio Code documentation: https://code.visualstudio.com/docs
