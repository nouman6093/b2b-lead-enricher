from urllib.parse import urlparse
import dns.resolver

JUNK_EXTENSIONS = (".png", ".jpg", ".jpeg", ".gif", ".svg", ".webp", ".css", ".js")
JUNK_DOMAINS = ("sentry.io", "example.com", "wixpress.com", "domain.com", "email.com")
JUNK_PREFIXES = ("noreply", "no-reply", "donotreply", "mailer-daemon")
PRIORITY_PREFIXES = ("hello@", "contact@", "info@", "sales@", "hi@", "support@")


def clean_and_select_email(emails: list[str], website: str) -> str:
    root_domain = urlparse(website).netloc.replace("www.", "").lower()
    valid = []

    for email in emails:
        if any(email.endswith(ext) for ext in JUNK_EXTENSIONS):
            continue
        if any(bad in email for bad in JUNK_DOMAINS):
            continue
        if email.startswith(JUNK_PREFIXES):
            continue
        valid.append(email)

    if not valid:
        return "Not Found"

    # Prefer emails matching the company's own domain and common contact prefixes
    domain_matches = [e for e in valid if root_domain and root_domain in e]
    pool = domain_matches if domain_matches else valid

    for prefix in PRIORITY_PREFIXES:
        for email in pool:
            if email.startswith(prefix):
                return email

    return pool[0]


def verify_mx_record(email: str) -> str:
    if "@" not in email:
        return "No Email Found"
    domain = email.split("@")[-1]
    try:
        records = dns.resolver.resolve(domain, "MX")
        return "Valid (MX Verified)" if records else "Invalid MX"
    except Exception:
        return "Unverified / No MX"