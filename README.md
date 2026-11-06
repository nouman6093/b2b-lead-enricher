# B2B Lead Scraper & Website Email Enricher

An asynchronous Python pipeline that takes raw company domains, crawls key pages (`/`, `/contact`, `/about`), extracts verified business contact details and LinkedIn profiles, validates email deliverability via DNS MX records, and exports a clean, client-ready Excel deliverable.

## Business Problem Solved
Raw lead lists often lack direct contact channels or contain dead domains that hurt sender reputation. This pipeline automates website enrichment and MX-level verification—turning raw company URLs into outreach-ready B2B prospect sheets.

## Pipeline Architecture
1. **Async Web Crawler (`src/crawler.py`):** Concurrently fetches each company's homepage, `/contact`, and `/about` routes using `httpx`.
2. **Contact & Social Extractor (`src/extractor.py`):** Parses HTML `mailto:`, `tel:`, and structured text via `BeautifulSoup` & regex to extract emails, phone numbers, and LinkedIn company URLs.
3. **Junk Filter & MX Validator (`src/validator.py`):** Strips image/script false positives, prioritizes primary business inboxes (`hello@`, `contact@`, `info@`), and verifies active mail servers via `dnspython`.
4. **Formatted Excel Export (`main.py`):** Outputs an auto-sized, clean `.xlsx` file ready for CRM import or outbound campaigns.

## Sample Output

| Company | Website | Verified Email | Deliverability Status | Phone | LinkedIn URL |
| :--- | :--- | :--- | :--- | :--- | :--- |
| WebFX | https://www.webfx.com | info@webfx.com | Valid (MX Verified) | 888-601-5359 | https://www.linkedin.com/company/webfxinc |
| Single Grain | https://www.singlegrain.com | contact@singlegrain.com | Valid (MX Verified) | Not Found | https://www.linkedin.com/company/single-grain |

## Quickstart

```bash
pip install -r requirements.txt
python main.py