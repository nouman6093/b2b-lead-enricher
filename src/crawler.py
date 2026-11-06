import asyncio
from urllib.parse import urljoin
import httpx

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36"
    )
}
TARGET_PATHS = ["", "/contact", "/contact-us", "/about"]


async def _fetch_page(client: httpx.AsyncClient, url: str) -> str:
    try:
        response = await client.get(url, timeout=10.0, follow_redirects=True)
        if response.status_code == 200 and "text/html" in response.headers.get("content-type", ""):
            return response.text
    except httpx.HTTPError:
        pass
    return ""


async def crawl_domain(base_url: str, semaphore: asyncio.Semaphore) -> list[str]:
    if not base_url.startswith(("http://", "https://")):
        base_url = f"https://{base_url}"

    urls = [urljoin(base_url.rstrip("/") + "/", path.lstrip("/")) for path in TARGET_PATHS]

    async with semaphore:
        async with httpx.AsyncClient(headers=HEADERS) as client:
            pages = await asyncio.gather(*[_fetch_page(client, url) for url in urls])

    return [html for html in pages if html]