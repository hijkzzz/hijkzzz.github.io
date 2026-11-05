"""Publish assets under content-derived filenames so cached pages stay consistent."""

from hashlib import sha256
from pathlib import Path
import re


ROOT = Path(__file__).resolve().parents[1]
ASSETS = (
    ("assets/home.css", "index.html", "/assets/", "href"),
)


for source_name, page_name, url_prefix, attribute in ASSETS:
    source = ROOT / source_name
    data = source.read_bytes()
    digest = sha256(data).hexdigest()[:12]
    output = source.with_name(f"{source.stem}.{digest}{source.suffix}")
    page = ROOT / page_name
    pattern = (
        attribute + '="' + re.escape(url_prefix + source.stem)
        + r'(?:\.[0-9a-f]{12})?' + re.escape(source.suffix) + r'(?:\?[^\"]*)?"'
    )
    html, count = re.subn(
        pattern, f'{attribute}="{url_prefix}{output.name}"', page.read_text()
    )
    if count != 1:
        raise ValueError(f"Expected one asset reference in {page_name}, got {count}")
    output.write_bytes(data)
    page.write_text(html)
    print(f"{page_name}: {url_prefix}{output.name}")
