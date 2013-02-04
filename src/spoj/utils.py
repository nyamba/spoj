import htmlentitydefs, re


def unescape(text):
    def fixup(m):
        text = m.group(0)
        if text[:2] == "&#":
            # character reference
            try:
                if text[:3] == "&#x":
                    return unichr(int(text[3:-1], 16))
                else:
                    return unichr(int(text[2:-1]))
            except ValueError:
                pass
        else:
            # named entity
            try:
                text = unichr(htmlentitydefs.name2codepoint[text[1:-1]])
            except KeyError:
                pass
        return text # leave as is
    return re.sub("&#?\w+;", fixup, text)


def text_table(soup_table, table_printer, skip_row=0):
    t = table_printer

    rows = soup_table.findAll('tr')[skip_row:]
    for r in rows:
        cells = r.findAll('td')
        t.add_row([unescape(c.text) for c in cells])

    return t
