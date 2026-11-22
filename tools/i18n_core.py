# -*- coding: utf-8 -*-
"""Общее ядро: выделение переводимых строк из страниц сайта и подстановка переводов."""
import re
from bs4 import BeautifulSoup, NavigableString, Comment

INLINE = {'a','b','strong','em','i','u','span','small','sup','sub','br','mark','code','s'}
SKIP = {'script','style','noscript','svg','path','head'}
ATTRS = ('alt','title','aria-label','placeholder')
CYR = re.compile(r'[А-Яа-яЁё]')

def norm(s):
    return re.sub(r'\s+', ' ', s).strip()

def inner(el):
    return norm(''.join(str(c) for c in el.contents))

def has_cyr(s): return bool(CYR.search(s))

def units(soup):
    """Возвращает список (kind, element_or_node, attr, key)."""
    out = []
    body = soup.body
    def walk(el):
        if el.name in SKIP: return
        children = [c for c in el.children]
        direct_text = [c for c in children if isinstance(c, NavigableString) and not isinstance(c, Comment) and c.strip()]
        child_tags = [c for c in children if getattr(c, 'name', None)]
        all_inline = all(c.name in INLINE for c in child_tags)
        if direct_text and all_inline and el.name not in INLINE | {'body'}:
            key = inner(el)
            if has_cyr(key): out.append(('el', el, None, key))
            for c in child_tags:   # атрибуты внутри (alt/title) тоже
                pass
        else:
            for c in children:
                if isinstance(c, NavigableString) and not isinstance(c, Comment) and c.strip() and has_cyr(str(c)):
                    out.append(('text', c, None, norm(str(c))))
                elif getattr(c, 'name', None):
                    walk(c)
            return
        # внутренние теги с атрибутами
        for c in child_tags: attrs_of(c)
    def attrs_of(el):
        for a in ATTRS:
            v = el.get(a)
            if v and has_cyr(v): out.append(('attr', el, a, norm(v)))
        for c in getattr(el, 'children', []):
            if getattr(c, 'name', None): attrs_of(c)
    for el in body.find_all(True):
        for a in ATTRS:
            v = el.get(a)
            if v and has_cyr(v): out.append(('attr', el, a, norm(v)))
    walk(body)
    return out

def head_units(soup):
    out = []
    if soup.title and has_cyr(soup.title.get_text()): out.append(('title', soup.title, None, norm(soup.title.get_text())))
    for m in soup.find_all('meta'):
        k = m.get('name') or m.get('property')
        if k in ('description','og:title','og:description','og:site_name','twitter:title','twitter:description') and m.get('content') and has_cyr(m['content']):
            out.append(('meta', m, 'content', norm(m['content'])))
    return out

def all_units(html):
    soup = BeautifulSoup(html, 'html.parser')
    return soup, head_units(soup) + units(soup)

def extract_keys(pages):
    keys = []
    for p in pages:
        html = open(p, encoding='utf-8').read()
        _, us = all_units(html)
        for u in us:
            if u[3] not in keys: keys.append(u[3])
    return keys
