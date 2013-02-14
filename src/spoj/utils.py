import htmlentitydefs, re, pydoc, webbrowser, tempfile


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


def escape_sub(html):
    '''
    >>> escape_sub('<b>test</b> help x<sup>2+1</sup>')
    '<b>test</b> help x^(2+1)'
    >>> escape_sub('<b>test</b> help x<sub>2+1</sub>')
    '<b>test</b> help x[2+1]'
    >>> escape_sub('<b>test</b> help x<sup>2</sup>')
    '<b>test</b> help x^2'
    >>> escape_sub('a=y+x/(y<sup>2</sup>+|x<sup>2</sup>/(y+x<sup>3</sup>/3)|)')
    'a=y+x/(y^2+|x^2/(y+x^3/3)|)'
    '''

    def fix_sup(match_obj):
        cc = match_obj.group('cc')
        if len(cc) > 1:
            return '^(%s)' % cc
        else:
            return '^' + cc

    def fix_sub(match_obj):
        return '[%s]' % match_obj.group('cc')

    html = re.sub(r'\<sub\>(?P<cc>[a-z0-9*+/-_]*)\<\/sub\>', fix_sub, html, flags=re.I)
    html = re.sub(r'\<sup\>(?P<cc>[a-z0-9*+/-_]*)\<\/sup\>', fix_sup, html, flags=re.I)

    return html


def display_in_browser(html):
    _, fname= tempfile.mkstemp()
    fname = fname
    f = open(fname, 'w')
    f.write(html)
    f.close()
    webbrowser.open('file://'+fname)
