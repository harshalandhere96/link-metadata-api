
import ipaddress
import socket
from urllib.parse import urlparse

import requests
from bs4 import BeautifulSoup


class MetadataError(Exception):
    """Raised when webpage metadata cannot be extracted."""


def validate_public_url(url: str) -> str:
    """Allow only HTTP(S) URLs that resolve to public IP addresses."""
    try:
        parsed = urlparse(url)
        if parsed.scheme not in ("http", "https") or not parsed.hostname:
            raise MetadataError("Enter a valid HTTP or HTTPS URL.")

        if parsed.username or parsed.password:
            raise MetadataError("URLs containing credentials are not allowed.")

        host = parsed.hostname

        # Reject local hostnames and local/private IP addresses.
        if host.lower() == "localhost" or host.lower().endswith(".localhost"):
            raise MetadataError("Local URLs are not allowed.")

        try:
            ip = ipaddress.ip_address(host)
            addresses = [ip]
        except ValueError:
            try:
                results = socket.getaddrinfo(
                    host, None, type=socket.SOCK_STREAM
                )
                addresses = [
                    ipaddress.ip_address(item[4][0])
                    for item in results
                ]
            except socket.gaierror:
                raise MetadataError("The website hostname could not be resolved.")

        if not addresses or any(not ip.is_global for ip in addresses):
            raise MetadataError("Only publicly accessible websites are allowed.")

        return url

    except MetadataError:
        raise
    except (ValueError, TypeError):
        raise MetadataError("Enter a valid URL.")


def extract_metadata(url: str) -> dict:
    url = validate_public_url(url)

    try:
        response = requests.get(
            url,
            timeout=8,
            allow_redirects=False,
            headers={
                "User-Agent": "LinkMetadataDemo/1.0"
            },
        )
    except requests.RequestException:
        raise MetadataError("Unable to retrieve the webpage.")

    if 300 <= response.status_code < 400:
        raise MetadataError(
            "The website returned a redirect. Enter its final URL."
        )

    if response.status_code >= 400:
        raise MetadataError(
            f"The website returned HTTP {response.status_code}."
        )

    content_type = response.headers.get("Content-Type", "")
    if content_type and "html" not in content_type.lower():
        raise MetadataError("The URL does not return an HTML webpage.")

    html = response.text[:2_000_000]
    soup = BeautifulSoup(html, "html.parser")

    def meta_content(*names: str) -> str | None:
        for name in names:
            tag = soup.find("meta", attrs={"property": name})
            if not tag:
                tag = soup.find("meta", attrs={"name": name})
            if tag and tag.get("content"):
                return tag["content"].strip()
        return None

    title_tag = soup.find("title")
    title = (
        meta_content("og:title", "twitter:title")
        or (title_tag.get_text(strip=True) if title_tag else None)
    )

    description = meta_content(
        "og:description",
        "description",
        "twitter:description",
    )

    image = meta_content("og:image", "twitter:image")
    site_name = meta_content("og:site_name")

    return {
        "url": url,
        "title": title,
        "description": description,
        "image": image,
        "site_name": site_name,
    }
