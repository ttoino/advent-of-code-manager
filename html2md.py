import bs4
import re
from urllib.parse import urljoin


def html2md(html: bs4.element.Tag, part: int, base_url: str):
    for d in html.find_all(text=True):
        d: bs4.NavigableString
        d.replace_with(d.replace("*", "\\*").replace("`", "\\`"))

    for h in html.select("h2"):
        h.replace_with(
            f"{'#' * part} {h.text.removeprefix('--- ').removesuffix(' ---')}\n\n"
        )

    for pre in html.select("pre"):
        b = pre.select("em")

        if b:
            for b in b:
                b.replace_with(f"<strong>{b.text}</strong>")
            pre.replace_with(f"<pre><code>{pre.text}</code></pre>\n")
        else:
            t = pre.text + ('' if pre.text.endswith('\n') else '\n')
            pre.replace_with(f"```\n{t}```\n")

    for a in html.select("a"):
        url = urljoin(base_url, a.attrs['href'])
        a.replace_with(f"[{a.text}]({url})")

    for c in html.select("code"):
        b = c.select("em")

        if b:
            if len(b) == 1 and b[0].text == c.text:
                t = c.text.replace('\\*', '*')
                c.replace_with(f"**`{t}`**")
            else:
                for b in b:
                    b.replace_with(f"<strong>{b.text}</strong>")
                c.replace_with(f"<code>{c.text}</code>")
        else:
            t = c.text.replace('\\*', '*')
            c.replace_with(f"`{t}`")

    for b in html.select("em"):
        b.replace_with(f"**{b.text}**")

    for l in html.select(":scope > ul"):
        for li in l.select(":scope > li"):
            for ll in li.select(":scope > ul"):
                for lli in ll.select(":scope > li"):
                    lli.replace_with(f"  - {lli.text.replace('  ', ' ')}")
                ll.replace_with(ll.text.removesuffix("\n"))
            li.replace_with(f"- {re.sub(r'  (?!-)', ' ', li.text)}")
        l.replace_with(l.text.removeprefix("\n"))

    for p in html.select("p"):
        p.replace_with(f"{p.text.replace('  ', ' ')}\n")

    return html.text.removesuffix("\n")