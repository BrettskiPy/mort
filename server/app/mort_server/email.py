import os
import smtplib
from email.headerregistry import Address
from email.message import EmailMessage
from typing import Any, Dict, Optional, Union

import jinja2

from mort_server.config import settings


def send_email(
    email_to: str,
    subject_template: str = "",
    html_template: str = "",
    environment: Dict[str, Any] = {},
) -> None:
    assert settings.EMAILS_ENABLED, "Email is not enabled on this server"

    email_to_ = email_to.split("@")

    template = render_template(html_template, values=environment)

    msg = EmailMessage()
    msg["From"] = Address(
        settings.EMAIL_FROM_NAME, settings.EMAIL_FROM_USER, settings.EMAIL_FROM_DOMAIN
    )
    msg["Subject"] = subject_template
    msg["To"] = Address(username=email_to_[0].strip(), domain=email_to_[1].strip())
    msg.add_alternative(template, subtype="html")

    server: Optional[Union[smtplib.SMTP_SSL, smtplib.SMTP]] = None
    try:
        if settings.SMTP_TLS:
            server = smtplib.SMTP_SSL(settings.SMTP_HOST, settings.SMTP_PORT)
        else:
            server = smtplib.SMTP(settings.SMTP_HOST, settings.SMTP_PORT)

        if settings.SMTP_USER and settings.SMTP_PASSWORD:
            server.login(settings.SMTP_USER, settings.SMTP_PASSWORD)

        response = server.send_message(msg)
    except Exception as e:
        raise RuntimeError(str(e))
    finally:
        if server:
            server.close()

    if response:
        raise ValueError(f"Failed to send email, got response: {response}")


def render_template(template_path: str, values: Dict[Any, Any] = None) -> str:
    # Ensure template exists
    if not os.path.exists(template_path):
        raise ValueError(f"No jinja template found at {template_path}")

    template_loader = jinja2.FileSystemLoader(searchpath="/")
    template_env = jinja2.Environment(loader=template_loader)
    template = template_env.get_tempalte(template_path)
    return template.render(values)
