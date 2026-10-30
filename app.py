import os
import re
import smtplib
import ssl
from email.message import EmailMessage

import streamlit as st

st.set_page_config(page_title="Email Automation Tool", page_icon="✉️", layout="centered")

st.title("✉️ Email Automation Tool")
st.caption("A Python-based application for preparing and sending emails securely.")

# Read settings from Streamlit secrets first, then environment variables.
def setting(name: str, default: str = "") -> str:
    try:
        value = st.secrets.get(name, "")
        if value:
            return str(value)
    except Exception:
        pass
    return os.getenv(name, default)

def valid_email(address: str) -> bool:
    return bool(re.fullmatch(r"[A-Za-z0-9.!#$%&'*+/=?^_`{|}~-]+@[A-Za-z0-9](?:[A-Za-z0-9-]{0,61}[A-Za-z0-9])?(?:\.[A-Za-z0-9](?:[A-Za-z0-9-]{0,61}[A-Za-z0-9])?)+", address.strip()))

with st.expander("SMTP configuration", expanded=False):
    st.write("Configure your email provider before sending. Credentials are read from Streamlit Secrets or environment variables; do not put passwords in source code.")
    st.code("SMTP_HOST = smtp.gmail.com\nSMTP_PORT = 465\nSMTP_USERNAME = your_email@gmail.com\nSMTP_PASSWORD = your_app_password", language="text")
    st.caption("For Gmail, use an App Password where supported; do not use your normal account password. Provider settings may differ.")

smtp_host = setting("SMTP_HOST", "smtp.gmail.com")
smtp_port_raw = setting("SMTP_PORT", "465")
smtp_username = setting("SMTP_USERNAME")
smtp_password = setting("SMTP_PASSWORD")
from_email = setting("FROM_EMAIL", smtp_username)

try:
    smtp_port = int(smtp_port_raw)
except (TypeError, ValueError):
    smtp_port = 465

if not smtp_username or not smtp_password:
    st.info("SMTP credentials are not configured yet. Add SMTP_USERNAME and SMTP_PASSWORD to Streamlit Secrets or environment variables to enable sending.")
else:
    st.success(f"SMTP configuration found for {smtp_username}")

with st.form("email_form", clear_on_submit=False):
    recipient = st.text_input("Recipient email address", placeholder="recipient@example.com")
    subject = st.text_input("Subject", placeholder="Enter email subject")
    body = st.text_area("Message", height=220, placeholder="Write your email message here...")
    submitted = st.form_submit_button("Send email", type="primary", use_container_width=True)

if submitted:
    errors = []
    if not valid_email(recipient):
        errors.append("Enter a valid recipient email address.")
    if not subject.strip():
        errors.append("Subject cannot be empty.")
    if not body.strip():
        errors.append("Message cannot be empty.")
    if not smtp_username or not smtp_password:
        errors.append("SMTP credentials are not configured.")
    if not from_email or not valid_email(from_email):
        errors.append("Configure a valid FROM_EMAIL (or SMTP_USERNAME).")
    if smtp_port not in (465, 587):
        errors.append("Use SMTP port 465 (SSL) or 587 (STARTTLS), as supported by your provider.")

    if errors:
        for error in errors:
            st.error(error)
    else:
        message = EmailMessage()
        message["From"] = from_email
        message["To"] = recipient.strip()
        message["Subject"] = subject.strip()
        message.set_content(body.strip())

        try:
            context = ssl.create_default_context()
            if smtp_port == 465:
                with smtplib.SMTP_SSL(smtp_host, smtp_port, context=context, timeout=20) as server:
                    server.login(smtp_username, smtp_password)
                    server.send_message(message)
            else:
                with smtplib.SMTP(smtp_host, smtp_port, timeout=20) as server:
                    server.ehlo()
                    server.starttls(context=context)
                    server.ehlo()
                    server.login(smtp_username, smtp_password)
                    server.send_message(message)
            st.success("Email submitted to the configured email server successfully.")
            st.caption("This confirms server submission, not guaranteed delivery to the recipient's inbox.")
        except (smtplib.SMTPException, OSError, TimeoutError) as exc:
            # Do not show credentials or full debug traces to the user.
            st.error("The email could not be sent. Check SMTP settings, authentication, network access, and provider restrictions.")
            st.caption(f"Error type: {type(exc).__name__}")

st.divider()
st.caption("Use this tool only for legitimate messages to recipients who expect or have agreed to receive them. Avoid bulk unsolicited email.")
