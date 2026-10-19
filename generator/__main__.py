"""Build the site with: python -m generator."""

from html import escape
from pathlib import Path
from string import Template
from tempfile import TemporaryDirectory
from shutil import copyfile
from urllib.parse import quote

import yaml

from .markdown import render_body
from .links import page_url, resolve_link


ROOT = Path(__file__).resolve().parent.parent
DEFAULT_LANGUAGE = "zh"
LANGUAGES = {"zh": "中文", "en": "English"}


def read_page(source: Path) -> tuple[str, str]:
    lines = source.read_text(encoding="utf-8").splitlines()
    if not lines or lines[0] != "---":
        raise ValueError(f"{source}: missing YAML front matter")
    try:
        end = lines.index("---", 1)
    except ValueError as error:
        raise ValueError(f"{source}: unclosed YAML front matter") from error
    metadata = yaml.safe_load("\n".join(lines[1:end]))
    if not isinstance(metadata, dict):
        raise ValueError(f"{source}: metadata must be a mapping")
    title = metadata.get("title")
    if not isinstance(title, str) or not title.strip():
        raise ValueError(f"{source}: title must be non-empty text")
    return title, "\n".join(lines[end + 1:])


def output_path(language: str, relative: Path) -> Path:
    directory = relative.parent if relative.stem == "index" else relative.with_suffix("")
    prefix = Path() if language == DEFAULT_LANGUAGE else Path(language)
    return prefix / directory / "index.html"


def build() -> Path:
    content = (ROOT / "content").resolve()
    pages = {}
    destinations = set()
    for source in sorted(content.rglob("*.md")):
        relative = source.relative_to(content)
        language = DEFAULT_LANGUAGE
        if len(relative.parts) > 1 and relative.parts[0] in LANGUAGES and relative.parts[0] != DEFAULT_LANGUAGE:
            language, relative = relative.parts[0], Path(*relative.parts[1:])
        destination = output_path(language, relative)
        if language == DEFAULT_LANGUAGE and destination.parts[0] in LANGUAGES and destination.parts[0] != DEFAULT_LANGUAGE:
            raise ValueError(f"{source}: output path is reserved for a translation language")
        if destination.parts[0] == "assets":
            raise ValueError(f"{source}: /assets/ is reserved for resources")
        if destination in destinations:
            raise ValueError(f"{source}: duplicate output path {destination}")
        destinations.add(destination)
        pages[language, relative] = (source, destination)
    if not pages:
        raise ValueError("No Markdown pages found")
    if (DEFAULT_LANGUAGE, Path("index.md")) not in pages:
        raise ValueError("content/index.md is required for the default homepage")

    source_outputs = {source.resolve(): destination for source, destination in pages.values()}
    asset_root = (ROOT / "assets").resolve()
    assets = {}
    for asset in sorted(asset_root.rglob("*")):
        if asset.is_symlink():
            raise ValueError(f"{asset}: asset symlinks are not supported")
        if asset.is_file() and asset.name != ".gitkeep":
            assets[asset.resolve()] = "/assets/" + quote(asset.relative_to(asset_root).as_posix())

    template = Template((ROOT / "templates/page.html").read_text(encoding="utf-8"))
    output = ROOT / "dist"
    with TemporaryDirectory(prefix=".build-", dir=ROOT) as temporary:
        staging = Path(temporary) / "site"
        staging.mkdir()
        for (language, relative), (source, destination) in pages.items():
            title, markdown = read_page(source)
            body = render_body(
                markdown,
                lambda url: resolve_link(url, source, content, source_outputs, assets),
            )
            links = []
            for other, label in LANGUAGES.items():
                counterpart = pages.get((other, relative))
                if other != language and counterpart:
                    url = escape(page_url(counterpart[1]), quote=True)
                    links.append(f'<a href="{url}" lang="{other}" hreflang="{other}">{label}</a>')
            navigation_label = "语言" if language == "zh" else "Language"
            page = template.substitute(
                language=language,
                title=escape(title),
                body=body,
                translations=f'<nav aria-label="{navigation_label}">' + " ".join(links) + '</nav>' if links else "",
            )
            target = staging / destination
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_text(page, encoding="utf-8")
        for asset in assets:
            target = staging / "assets" / asset.relative_to(asset_root)
            target.parent.mkdir(parents=True, exist_ok=True)
            copyfile(asset, target)
        backup = Path(temporary) / "previous"
        if output.exists():
            output.rename(backup)
        try:
            staging.rename(output)
        except OSError:
            if backup.exists():
                backup.rename(output)
            raise
    return output


if __name__ == "__main__":
    print(f"Built {build().relative_to(ROOT)}/")
