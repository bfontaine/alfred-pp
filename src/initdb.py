#! /usr/bin/env python
# -*- coding: UTF-8 -*-

from alp import Request, jsonDump

def parse_liafa():
    """
    Return a list of people from LIAFA
    """
    people_list = []
    base = 'http://www.liafa.univ-paris-diderot.fr/'
    p_sel = 'blockquote > table tr.fondgristresc td:first-child a'
    page = Request(base + '/web9/membreliafa/listalpha_fr.php')
    page.download()
    page = page.souper()
    urls = [p.get('href') for p in page.find_all(p_sel)]

    for u in urls:
        if u == None:
            continue
        p = {}
        page = Request(base + u)
        page.download()
        page = page.souper()
        pp = page.find('table.texte li a.bleu')
        if (pp):
            p['url'] = pp.get('href')
            p['name'] = page.find('blockquote h2').get_text().strip()
            p['icon'] = 'liafa.png'
            people_list.append(pp)

    return people_list

def parse_pps():
    """
    Return a list of people from PPS
    """
    people_list = []
    base = 'http://www.pps.univ-paris-diderot.fr/'
    page = Request(base + '/membres')
    page.download()
    page = page.souper()
    pp = page.find('table a.ocsimore_phrasing_link')
    return [{
        'name': pp.get_text().strip(),
        'url': base+pp.get('href'),
        'icon': 'pps.png'} for p in pp]

def parse_all():
    return parse_liafa()+parse_pps()

def save_list():
    jsonDump(parse_all(), "people_list.json")
