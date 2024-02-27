"""Cross-references module."""

from __future__ import annotations

import re
from html import escape, unescape
from typing import TYPE_CHECKING, Any, Callable, Match
from urllib.parse import urlsplit
from xml.etree.ElementTree import Element

import markupsafe
from markdown.extensions import Extension
from markdown.inlinepatterns import REFERENCE_RE, ReferenceInlineProcessor
from markdown.util import HTML_PLACEHOLDER_RE, INLINE_PLACEHOLDER_RE

if TYPE_CHECKING:
    from markdown import Markdown

_ATTR_VALUE = r'"[^"<>]+"|[^"<> ]+'  # Possibly with double quotes around
AUTO_REF_RE = re.compile(
    rf"<span data-(?P<kind>autorefs-(?:identifier|optional|optional-hover))=(?P<identifier>{_ATTR_VALUE})"
    rf"(?: class=(?P<class>{_ATTR_VALUE}))?(?P<attrs> [^<>]+)?>(?P<title>.*?)</span>",
    flags=re.DOTALL,
)
"""A regular expression to match mkdocs-autorefs' special reference markers
in the [`on_post_page` hook][mkdocs_autorefs.plugin.AutorefsPlugin.on_post_page].
"""


class AutoRefInlineProcessor(ReferenceInlineProcessor):
    """A Markdown extension."""

    def __init__(self, *args: Any, **kwargs: Any) -> None:  # noqa: D107
        super().__init__(REFERENCE_RE, *args, **kwargs)

    # Code based on
    # https://github.com/Python-Markdown/markdown/blob/8e7528fa5c98bf4652deb13206d6e6241d61630b/markdown/inlinepatterns.py#L780

    def handleMatch(self, m: Match[str], data: str) -> tuple[Element | None, int | None, int | None]:  # type: ignore[override]  # noqa: N802
        """Handle an element that matched.

        Arguments:
            m: The match object.
            data: The matched data.

        Returns:
            A new element or a tuple.
        """
        text, index, handled = self.getText(data, m.end(0))
        if not handled:
            return None, None, None

        identifier, end, handled = self.evalId(data, index, text)
        if not handled or identifier is None:
            return None, None, None

        if re.search(r"[/ \x00-\x1f]", identifier):
            # Do nothing if the matched reference contains:
            # - a space, slash or control character (considered unintended);
            # - specifically \x01 is used by Python-Markdown HTML stash when there's inline formatting,
            #   but references with Markdown formatting are not possible anyway.
            return None, m.start(0), end

        return self._make_tag(identifier, text), m.start(0), end

    def evalId(self, data: str, index: int, text: str) -> tuple[str | None, int, bool]:  # noqa: N802 (parent's casing)
        """Evaluate the id portion of `[ref][id]`.

        If `[ref][]` use `[ref]`.

        Arguments:
            data: The data to evaluate.
            index: The starting position.
            text: The text to use when no identifier.

        Returns:
            A tuple containing the identifier, its end position, and whether it matched.
        """
        m = self.RE_LINK.match(data, pos=index)
        if not m:
            return None, index, False

        identifier = m.group(1)
        if not identifier:
            identifier = text
            # Allow the entire content to be one placeholder, with the intent of catching things like [`Foo`][].
            # It doesn't catch [*Foo*][] though, just due to the priority order.
            # https://github.com/Python-Markdown/markdown/blob/1858c1b601ead62ed49646ae0d99298f41b1a271/markdown/inlinepatterns.py#L78
            if match := INLINE_PLACEHOLDER_RE.fullmatch(identifier):
                stashed_nodes: dict[str, Element | str] = self.md.treeprocessors["inline"].stashed_nodes  # type: ignore[attr-defined]
                el = stashed_nodes.get(match[1])
                if isinstance(el, Element) and el.tag == "code":
                    identifier = "".join(el.itertext())
                    # Special case: allow pymdownx.inlinehilite raw <code> snippets but strip them back to unhighlighted.
                    if match := HTML_PLACEHOLDER_RE.fullmatch(identifier):
                        stash_index = int(match.group(1))
                        html = self.md.htmlStash.rawHtmlBlocks[stash_index]
                        identifier = markupsafe.Markup(html).striptags()
                        self.md.htmlStash.rawHtmlBlocks[stash_index] = escape(identifier)

        end = m.end(0)
        return identifier, end, True

    def _make_tag(self, identifier: str, text: str) -> Element:
        """Create a tag that can be matched by `AUTO_REF_RE`.

        Arguments:
            identifier: The identifier to use in the HTML property.
            text: The text to use in the HTML tag.

        Returns:
            A new element.
        """
        el = Element("span")
        el.set("data-autorefs-identifier", identifier)
        el.text = text
        return el


def relative_url(url_a: str, url_b: str) -> str:
    """Compute the relative path from URL A to URL B.

    Arguments:
        url_a: URL A.
        url_b: URL B.

    Returns:
        The relative URL to go from A to B.
    """
    parts_a = url_a.split("/")
    url_b, anchor = url_b.split("#", 1)
    parts_b = url_b.split("/")

    # remove common left parts
    while parts_a and parts_b and parts_a[0] == parts_b[0]:
        parts_a.pop(0)
        parts_b.pop(0)

    # go up as many times as remaining a parts' depth
    levels = len(parts_a) - 1
    parts_relative = [".."] * levels + parts_b
    relative = "/".join(parts_relative)
    return f"{relative}#{anchor}"


def fix_ref(url_mapper: Callable[[str], str], unmapped: list[str]) -> Callable:
    """Return a `repl` function for [`re.sub`](https://docs.python.org/3/library/re.html#re.sub).

    In our context, we match Markdown references and replace them with HTML links.

    When the matched reference's identifier was not mapped to an URL, we append the identifier to the outer
    `unmapped` list. It generally means the user is trying to cross-reference an object that was not collected
    and rendered, making it impossible to link to it. We catch this exception in the caller to issue a warning.

    Arguments:
        url_mapper: A callable that gets an object's site URL by its identifier,
            such as [mkdocs_autorefs.plugin.AutorefsPlugin.get_item_url][].
        unmapped: A list to store unmapped identifiers.

    Returns:
        The actual function accepting a [`Match` object](https://docs.python.org/3/library/re.html#match-objects)
        and returning the replacement strings.
    """

    def inner(match: Match) -> str:
        identifier = match["identifier"].strip('"')
        title = match["title"]
        kind = match["kind"]
        attrs = match["attrs"] or ""
        classes = (match["class"] or "").strip('"').split()

        try:
            url = url_mapper(unescape(identifier))
        except KeyError:
            if kind == "autorefs-optional":
                return title
            if kind == "autorefs-optional-hover":
                return f'<span title="{identifier}">{title}</span>'
            unmapped.append(identifier)
            if title == identifier:
                return f"[{identifier}][]"
            return f"[{title}][{identifier}]"

        parsed = urlsplit(url)
        external = parsed.scheme or parsed.netloc
        classes = ["autorefs", "autorefs-external" if external else "autorefs-internal", *classes]
        class_attr = " ".join(classes)
        if kind == "autorefs-optional-hover":
            return f'<a class="{class_attr}" title="{identifier}" href="{escape(url)}"{attrs}>{title}</a>'
        return f'<a class="{class_attr}" href="{escape(url)}"{attrs}>{title}</a>'

    return inner


def fix_refs(html: str, url_mapper: Callable[[str], str]) -> tuple[str, list[str]]:
    """Fix all references in the given HTML text.

    Arguments:
        html: The text to fix.
        url_mapper: A callable that gets an object's site URL by its identifier,
            such as [mkdocs_autorefs.plugin.AutorefsPlugin.get_item_url][].

    Returns:
        The fixed HTML.
    """
    unmapped: list[str] = []
    html = AUTO_REF_RE.sub(fix_ref(url_mapper, unmapped), html)
    return html, unmapped


class AutorefsExtension(Extension):
    """Extension that inserts auto-references in Markdown."""

    def extendMarkdown(self, md: Markdown) -> None:  # noqa: N802 (casing: parent method's name)
        """Register the extension.

        Add an instance of our [`AutoRefInlineProcessor`][mkdocs_autorefs.references.AutoRefInlineProcessor] to the Markdown parser.

        Arguments:
            md: A `markdown.Markdown` instance.
        """
        md.inlinePatterns.register(
            AutoRefInlineProcessor(md),
            "mkdocs-autorefs",
            priority=168,  # Right after markdown.inlinepatterns.ReferenceInlineProcessor
        )
