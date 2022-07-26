import bs4


def html2md(html: bs4.element.Tag, part: int):
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
            pre.replace_with(f"```\n{pre.text}```\n")

    for a in html.select("a"):
        a.replace_with(f"[{a.text}]({a.attrs['href']})")

    for c in html.select("code"):
        b = c.select("em")

        if b:
            if len(b) == 1 and b[0].text == c.text:
                c.replace_with(f"**`{c.text}`**")
            else:
                for b in b:
                    b.replace_with(f"<strong>{b.text}</strong>")
                c.replace_with(f"<code>{c.text}</code>")
        else:
            c.replace_with(f"`{c.text}`")

    for b in html.select("em"):
        b.replace_with(f"**{b.text}**")

    for l in html.select(":scope > ul"):
        for li in l.select(":scope > li"):
            for ll in li.select(":scope > ul"):
                for lli in ll.select(":scope > li"):
                    lli.replace_with(f"  - {lli.text}")
                ll.replace_with(ll.text.removesuffix("\n"))
            li.replace_with(f"- {li.text}")
        l.replace_with(l.text.removeprefix("\n"))

    for p in html.select("p"):
        p.replace_with(f"{p.text}\n")

    return html.text.removesuffix("\n")