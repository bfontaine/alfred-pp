"""
This module provide utilities to update the local list of people. This list is
stored as JSON in people.json, and each person is a dict with these keys:
'name' (the person name), 'url' (its personal page URL), 'icon' (an icon
path), 'info' (more info about this person; may be empty), and an optional key,
'fuzzy', which can be used for fuzzy matching.
"""

import re
import alp
from alp import Request, jsonDump, jsonLoad
from unidecode import unidecode
from urlparse import urljoin

JSON_LIST='people.json'

def fmt_phone(ph):
    """
    Format a (French) phone number
    """
    ph = re.sub('^(\+?33\s(?:\(?0\)?))', '0', ph)
    return re.sub('(?<=\d)[-. ](?=\d)', '.', ph).strip()

def fmt_name(n):
    """
    Format a name
    """
    return re.sub('([A-Z]{3,})', lambda m: m.group(1).capitalize(), n)

def text(el):
    """
    Helper to get the text content of a BeautifulSoup item
    """
    return el.get_text().strip()

def mk_fuzzy(p):
    """
    Return the 'fuzzy' field of a person dict
    """
    els = []
    els.append(p['name'])
    els.append(unidecode(p['name']))
    if 'url' in p:
        urlname = re.search('/~(\w+)', p['url'])
        if urlname:
            els.append(urlname.group(1))
    return els.join(' ## ')

def parse_liafa():
    """
    Return a list of people from LIAFA.
    """
    icon = alp.local('liafa.png')
    people_list = []
    base = 'http://www.liafa.univ-paris-diderot.fr/'
    tr_sel = 'blockquote > table tr.fondgristresc' # td:first-child a'
    page = Request(urljoin(base, '/web9/membreliafa/listalpha_fr.php'))
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
        tds = tr.select('td.texte')
        if len(tds) >= 2:
            p['info'] = 'Office ' + text(tds[1]) \
                      + ', phone: ' + fmt_phone(text(tds[0]))
        page = Request(base + u)
        page.download()
        page = page.souper()
        pp = page.select('table.texte li a.bleu')
        if (pp):
            pp = pp[0]
            p['url'] = urljoin(base, pp.get('href'))
            p['name'] = fmt_name(text(page.select('blockquote h2')[0]))
            p['icon'] = icon
            p['fileIcon'] = True
            p['fuzzy'] = p['name']
            people_list.append(p)

    return people_list


def parse_pps():
    """
    Return a list of people from PPS
    """
    icon = alp.local('pps.png')
    people_list = []
    base = 'http://www.pps.univ-paris-diderot.fr'
    page = Request(base + '/membres')
    page.download()
    page = page.souper()
    trs = page.select('#contenu2 table')[0].find_all('tr')[1:]

    for tr in trs:
        link = tr.find('a')
        if not link:
            continue
        p = {}
        p['url']  = urljoin(base, link.get('href'))
        p['name'] = fmt_name(text(link))
        p['fuzzy'] = p['name']
        p['icon'] = icon
        p['fileIcon'] = True

        tds = tr.find_all('td')
        if (len(tds) >= 4):
            p['info']  = 'Office ' + text(tds[2]) \
                       + ', phone: ' + fmt_phone('01 57 27 ' + text(tds[3]))

        people_list.append(p)

    return people_list

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
