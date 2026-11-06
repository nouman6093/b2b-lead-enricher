import re
from bs4 import BeautifulSoup

EMAIL_REGEX = re.compile(r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}")
PHONE_REGEX = re.compile(r"(?:\+?1[-.\s]?)?\(?\d{3}\)?[-.\s]\d{3}[-.\s]\d{4}")
LINKEDIN_REGEX = re.compile(r"https?://(?:www\.)?linkedin\.com/company/[a-zA-Z0-9_-]+/?")


def extract_contacts(html_pages: list[str]) -> dict:
    emails, phones, linkedins = set(), set(), set()

    for html in html_pages:
        soup = BeautifulSoup(html, "html.parser")

        for a in soup.find_all("a", href=True):
            href = a["href"].strip()
            if href.startswith("mailto:"):
                emails.add(href.replace("mailto:", "").split("?")[0].strip().lower())
            elif href.startswith("tel:"):
                phones.add(href.replace("tel:", "").strip())
            elif "linkedin.com/company/" in href:
                linkedins.add(href.split("?")[0].rstrip("/"))

        text = soup.get_text(" ", strip=True)
        emails.update(m.lower() for m in EMAIL_REGEX.findall(text))
        phones.update(m.strip() for m in PHONE_REGEX.findall(text))
        linkedins.update(m.rstrip("/") for m in LINKEDIN_REGEX.findall(html))

    return {
        "emails": list(emails),
        "phones": list(phones),
        "linkedin": next(iter(linkedins), "Not Found"),
    }