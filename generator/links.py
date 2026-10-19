"""Resolve source links to published page and asset URLs."""

from pathlib import Path
from urllib.parse import quote, unquote, urlsplit, urlunsplit


def page_url(path: Path) -> str:
    directory = path.parent.as_posix()
    return "/" if directory == "." else f"/{quote(directory)}/"


def resolve_link(url: str, source: Path, content: Path, pages: dict, assets: dict) -> str:
    parts = urlsplit(url)
    if parts.scheme or parts.netloc or not parts.path:
        return url
    path = unquote(parts.path)
    published = {page_url(output): page_url(output) for output in pages.values()}
    published.update({"/" + quote(output.as_posix()): page_url(output) for output in pages.values()})
    published.update({target: target for target in assets.values()})
    if path.startswith("/") and quote(path) in published:
        target = published[quote(path)]
    else:
        local = (content / path.lstrip("/") if path.startswith("/") else source.parent / path).resolve()
        if local in pages:
            target = page_url(pages[local])
        elif local in assets:
            target = assets[local]
        elif local / "index.md" in pages:
            target = page_url(pages[local / "index.md"])
        else:
            raise ValueError(f"{source}: missing or unpublished local target: {url}")
    return urlunsplit(("", "", target, parts.query, parts.fragment))
