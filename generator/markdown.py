from collections.abc import Callable

from markdown_it import MarkdownIt


def render_body(source: str, resolve_link: Callable[[str], str]) -> str:
    parser = MarkdownIt("commonmark", {"html": False})
    tokens = parser.parse(source)

    def rewrite(tokens):
        for token in tokens:
            attribute = {"link_open": "href", "image": "src"}.get(token.type)
            if attribute:
                url = token.attrGet(attribute)
                if url is not None:
                    token.attrSet(attribute, resolve_link(url))
            if token.children:
                rewrite(token.children)

    rewrite(tokens)
    return parser.renderer.render(tokens, parser.options, {})
