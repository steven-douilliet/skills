#!/usr/bin/env python3
"""Fetch a documentation page and convert it to readable markdown.

Usage:
    python3 fetchdoc.py <url> [--links]

- Tolerates self-signed / internal TLS certificates (e.g. *.lan docs sites).
- Extracts the <article> body when present (most doc generators: fumadocs,
  Docusaurus, MkDocs Material, ...), otherwise the whole page.
- Preserves code blocks (```), inline code (`), headings, lists and tables —
  i.e. exactly what matters when QA-ing a tutorial.
- With --links: instead of the text, prints the unique href list (handy to
  discover the table of contents / tutorial parts).

Why a script: the conversion is deterministic and was needed on every page of
the review. Re-generating this regex pipeline each time wastes tokens and
drifts.
"""
import html
import re
import ssl
import sys
import urllib.request


def fetch(url: str) -> str:
    ctx = ssl.create_default_context()
    ctx.check_hostname = False
    ctx.verify_mode = ssl.CERT_NONE
    req = urllib.request.Request(url, headers={"User-Agent": "tutorial-review/1.0"})
    return urllib.request.urlopen(req, context=ctx).read().decode("utf-8", "replace")


def to_markdown(raw_html: str) -> str:
    m = re.search(r"<article[^>]*>(.*?)</article>", raw_html, re.S)
    a = m.group(1) if m else raw_html
    a = re.sub(r"<pre[^>]*>", "\n```\n", a)
    a = re.sub(r"</pre>", "\n```\n", a)
    a = re.sub(r"<code[^>]*>", "`", a)
    a = re.sub(r"</code>", "`", a)
    for i in range(1, 7):
        a = re.sub(rf"<h{i}[^>]*>", "\n" + "#" * i + " ", a)
        a = re.sub(rf"</h{i}>", "\n", a)
    a = re.sub(r"<li[^>]*>", "\n- ", a)
    a = re.sub(r"</p>", "\n", a)
    a = re.sub(r"<br[^>]*>", "\n", a)
    a = re.sub(r"<tr[^>]*>", "\n| ", a)
    a = re.sub(r"</t[dh]>", " | ", a)
    a = re.sub(r"<[^>]+>", "", a)
    a = html.unescape(a)
    a = re.sub(r"[ \t]+\n", "\n", a)
    a = re.sub(r"\n{3,}", "\n\n", a)
    return a.strip()


def links(raw_html: str) -> str:
    found = sorted(set(re.findall(r'href="([^"]+)"', raw_html)))
    return "\n".join(h for h in found if not h.startswith(("#", "javascript:")))


def main() -> int:
    args = [x for x in sys.argv[1:] if not x.startswith("--")]
    if not args:
        print(__doc__)
        return 1
    raw = fetch(args[0])
    print(links(raw) if "--links" in sys.argv else to_markdown(raw))
    return 0


if __name__ == "__main__":
    sys.exit(main())
