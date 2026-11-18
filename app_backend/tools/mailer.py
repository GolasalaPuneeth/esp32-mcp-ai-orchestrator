import asyncio
import base64
import binascii
import mimetypes
import smtplib
from abc import ABC, abstractmethod
from email.message import EmailMessage
from pathlib import Path

from fastmcp.tools import tool

SMTP_HOST = "mailpit"
SMTP_PORT = 1025
SENDER_EMAIL = "puneeth3sprime@gmail.com"
MAX_ATTACHMENT_BYTES = 5 * 1024 * 1024  # 5 MB, measured after decoding


class MailServiceDoc(ABC):
    """Abstract interface defining email dispatch capabilities."""

    @abstractmethod
    async def send_html_email(
        self,
        recipient: str,
        subject: str,
        html_content: str,
        attachment_base64: str = None,
        attachment_name: str = None,
    ) -> bool:
        """
        Dispatch an HTML-formatted email via SMTP with an optional file attachment.

        Args:
            recipient (str): The destination email address.
            subject (str): The subject line of the email.
            html_content (str): The body of the email written in HTML format.
            attachment_base64 (str, optional): The file contents encoded as a
                base64 string. Must be sent together with attachment_name.
            attachment_name (str, optional): The file name, including its
                extension (for example "report.pdf"), used for the attachment
                and to detect its file type.

        Returns:
            bool: True if sent successfully, False otherwise. Returns False
                if the attachment is invalid, too large, or missing its name.
        """
        raise NotImplementedError


class MailService(MailServiceDoc):

    @tool()
    async def send_html_email(
        self,
        recipient: str,
        subject: str,
        html_content: str,
        attachment_base64: str = None,
        attachment_name: str = None,
    ) -> bool:
        """
        Send an HTML email via the local Mailpit SMTP server.
        To attach a file, pass its contents as a base64 string in
        attachment_base64 and its file name (with extension) in attachment_name.
        Both must be provided together. Returns True if the email was sent.
        """
        message = EmailMessage()
        message["From"] = SENDER_EMAIL
        message["To"] = recipient
        message["Subject"] = subject
        message.set_content(
            "This is a fallback plain-text version for email clients "
            "that do not support HTML."
        )
        message.add_alternative(html_content, subtype="html")

        # Optional attachment, received inline as base64 (no file paths).
        if attachment_base64 or attachment_name:
            if not attachment_base64 or not attachment_name:
                print("Attachment error: attachment_base64 and attachment_name "
                      "must be provided together")
                return False

            try:
                # Remove any whitespace or line breaks before decoding.
                cleaned = "".join(attachment_base64.split())
                file_data = base64.b64decode(cleaned, validate=True)
            except (binascii.Error, ValueError) as e:
                print(f"Attachment error: invalid base64 ({e})")
                return False

            if len(file_data) > MAX_ATTACHMENT_BYTES:
                print("Attachment error: file too large")
                return False

            file_name = Path(attachment_name).name  # drop any directory parts
            mime_type, _ = mimetypes.guess_type(file_name)
            maintype, subtype = (mime_type or "application/octet-stream").split("/", 1)
            message.add_attachment(
                file_data,
                maintype=maintype,
                subtype=subtype,
                filename=file_name,
            )

        def _send():
            with smtplib.SMTP(SMTP_HOST, SMTP_PORT) as server:
                server.send_message(message)

        try:
            # smtplib is blocking, so run it in a thread to keep the event loop free.
            await asyncio.to_thread(_send)
            print(f"Email sent to Mailpit at {SMTP_HOST}:{SMTP_PORT}")
            return True
        except Exception as e:
            print(f"Failed to send email: {e}")
            return False