import htmlentitydefs, re, pydoc


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


def text_table(soup_table, table_printer, skip_row=0,
        cell_formatter=lambda c: unescape(c.text)):
    t = table_printer

    rows = soup_table.findAll('tr')[skip_row:]
    for r in xrange(len(rows)):
        cells = rows[r].findAll('td')
        row = []
        for c in xrange(len(cells)):
            row.append(cell_formatter(r, c, cells[c]))

        t.add_row(row)

    return t


def pager(text):
    pydoc.pager(text.encode('utf-8'))
