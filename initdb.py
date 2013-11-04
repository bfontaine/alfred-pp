from alp import Request, jsonDump, jsonLoad

JSON_LIST='people.json'

def fmt_url(u, base=''):
    if u.startswith('http') or base == '':
        return u

    if u.startswith('/'):
        u = u[1:]

    if base.endswith('/'):
        return base + u

    return base[:-1] + u


def parse_liafa():
    """
    Return a list of people from LIAFA
    """
    people_list = []
    base = 'http://www.liafa.univ-paris-diderot.fr/'
    tr_sel = 'blockquote > table tr.fondgristresc' # td:first-child a'
    page = Request(fmt_url('/web9/membreliafa/listalpha_fr.php', base))
    page.download()
    page = page.souper()
    for tr in page.select(tr_sel):
        links = tr.select('td a')
        if (len(links) == 0):
            continue

        u = links[0].get('href')
        if u == None:
            continue
        p = {}
        page = Request(base + u)
        page.download()
        page = page.souper()
        pp = page.select('table.texte li a.bleu')
        if (pp):
            pp = pp[0]
            p['url'] = fmt_url(pp.get('href'), base)
            p['name'] = page.select('blockquote h2')[0].get_text().strip()
            p['icon'] = 'liafa.png'
            people_list.append(p)

    return people_list


def parse_pps():
    """
    Return a list of people from PPS
    """
    people_list = []
    base = 'http://www.pps.univ-paris-diderot.fr'
    page = Request(base + '/membres')
    page.download()
    page = page.souper()
    pp = page.select('table a.ocsimore_phrasing_link')
    return [{
        'name': p.get_text().strip(),
        'url': fmt_url(p.get('href'), base),
        'icon': 'pps.png'} for p in pp] if pp else []

def parse_all():
    return parse_liafa()+parse_pps()

def save_list():
    p = parse_all()
    jsonDump(p, JSON_LIST)
    return p

def get_list():
    li = jsonLoad(JSON_LIST, default=[])
    if len(li) == 0:
        return save_list()
    return li
