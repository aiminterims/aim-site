# -*- coding: utf-8 -*-
"""Генерирует языковые версии сайта (/en/, /kk/, /uz/, /hy/, /az/) из русских страниц и словарей i18n/<lang>.txt.
Запуск: python tools/build_i18n.py   (нужен beautifulsoup4)"""
import os, re, json, sys
from urllib.parse import urljoin, urlsplit
from bs4 import BeautifulSoup, NavigableString
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from i18n_core import all_units, norm, extract_keys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SITE = 'https://aim-interims.ru'
PAGES = [('index.html', '/'), ('school/index.html', '/school/'), ('products/index.html', '/products/')]
PAGE_URLS = {u for _, u in PAGES}

LANGS = {
 'en': dict(locale='en_US', name='English', org='Association of Interim Managers (AIM)', school='School of Interim Managers', person='Andrey Fomin',
            months=['January','February','March','April','May','June','July','August','September','October','November','December'], fmt='{d} {m}'),
 'kk': dict(locale='kk_KZ', name='Қазақша', org='Интерим-менеджерлер қауымдастығы (АИМ)', school='Интерим-менеджерлер мектебі', person='Андрей Фомин',
            months=['қаңтар','ақпан','наурыз','сәуір','мамыр','маусым','шілде','тамыз','қыркүйек','қазан','қараша','желтоқсан'], fmt='{d} {m}'),
 'uz': dict(locale='uz_UZ', name='Oʻzbekcha', org='Interim-menejerlar assotsiatsiyasi (AIM)', school='Interim-menejerlar maktabi', person='Andrey Fomin',
            months=['yanvar','fevral','mart','aprel','may','iyun','iyul','avgust','sentyabr','oktyabr','noyabr','dekabr'], fmt='{d}-{m}'),
 'hy': dict(locale='hy_AM', name='Հայերեն', org='Ինտերիմ մենեջերների ասոցիացիա (AIM)', school='Ինտերիմ մենեջերների դպրոց', person='Անդրեյ Ֆոմին',
            months=['հունվարի','փետրվարի','մարտի','ապրիլի','մայիսի','հունիսի','հուլիսի','օգոստոսի','սեպտեմբերի','հոկտեմբերի','նոյեմբերի','դեկտեմբերի'], fmt='{m} {d}'),
 'az': dict(locale='az_AZ', name='Azərbaycanca', org='İnterim Menecerlər Assosiasiyası (AIM)', school='İnterim menecerlər məktəbi', person='Andrey Fomin',
            months=['yanvar','fevral','mart','aprel','may','iyun','iyul','avqust','sentyabr','oktyabr','noyabr','dekabr'], fmt='{d} {m}'),
}
RU_MONTHS = ['января','февраля','марта','апреля','мая','июня','июля','августа','сентября','октября','ноября','декабря']
RU_ORG = 'Ассоциация Интерим Менеджеров'
RU_SCHOOL = 'Школа интерим-менеджеров'

def load_dict(lang, keys):
    d = {}
    p = os.path.join(ROOT, 'i18n', lang + '.txt')
    for ln in open(p, encoding='utf-8'):
        ln = ln.rstrip('\n')
        if not ln.strip(): continue
        n, t = ln.split('|', 1)
        n = int(n)
        if n <= len(keys) and t != '=': d[keys[n-1]] = t
    return d

HREFLANG = '<!--hreflang-->'
def hreflang_block(path):
    out = [HREFLANG]
    out.append('<link rel="alternate" hreflang="ru" href="%s%s">' % (SITE, path))
    for l in LANGS: out.append('<link rel="alternate" hreflang="%s" href="%s/%s%s">' % (l, SITE, l, path))
    out.append('<link rel="alternate" hreflang="x-default" href="%s%s">' % (SITE, path))
    out.append('<!--/hreflang-->')
    return ''.join(out)

def set_inner(el, html):
    el.clear()
    frag = BeautifulSoup(html, 'html.parser')
    for c in list(frag.contents): el.append(c.extract())

def rewrite_url(v, base, lang):
    if not v: return v
    if re.match(r'^(https?:|//|mailto:|tel:|#|data:|javascript:)', v): return v
    full = urljoin('https://x' + base, v)
    u = urlsplit(full)
    path = u.path
    if path.endswith('index.html'): path = path[:-10]
    tail = ('?' + u.query if u.query else '') + ('#' + u.fragment if u.fragment else '')
    if path in PAGE_URLS: return '/' + lang + path + tail
    return path + tail

def translate_json(o, tr, lang, L):
    if isinstance(o, dict):
        if '@graph' in o:
            o = dict(o); o['@graph'] = [n for n in o['@graph'] if n.get('@type') not in ('FAQPage', 'Service', 'BreadcrumbList', 'ItemList')]
        return {k: translate_json(v, tr, lang, L) for k, v in o.items()}
    if isinstance(o, list): return [translate_json(v, tr, lang, L) for v in o]
    if isinstance(o, str):
        if o == 'ru': return lang
        if o == RU_ORG: return L['org']
        if o == RU_SCHOOL: return L['school']
        if o == 'Андрей Фомин': return L['person']
        n = norm(o)
        return tr.get(n, o)
    return o

def build_page(src, base, lang, tr):
    L = LANGS[lang]
    html = open(os.path.join(ROOT, src), encoding='utf-8').read()
    html = html.replace('url(assets/', 'url(/assets/')
    html = re.sub(r'<section id="faq">.*?</section>\n', '', html, flags=re.S)
    html = re.sub(re.escape(HREFLANG) + r'.*?<!--/hreflang-->', '', html, flags=re.S)
    soup, us = all_units(html)
    for kind, node, attr, key in us:
        t = tr.get(key)
        if not t: continue
        if kind == 'el': set_inner(node, t)
        elif kind == 'text': node.replace_with(NavigableString(t))
        elif kind == 'attr' or kind == 'meta': node[attr] = t
        elif kind == 'title': node.string = t
    # даты мероприятий
    for pill in soup.select('.pill.a'):
        m = re.match(r'^\s*(\d{1,2})\s+([а-яё]+)\s*$', pill.get_text())
        if m and m.group(2) in RU_MONTHS:
            i = RU_MONTHS.index(m.group(2))
            pill['data-d'] = '%02d-%02d' % (i+1, int(m.group(1)))
            pill.string = L['fmt'].format(d=int(m.group(1)), m=L['months'][i])
    # ссылки и ресурсы
    for el in soup.find_all(True):
        for a in ('href', 'src', 'poster', 'data-src'):
            if el.get(a): el[a] = rewrite_url(el[a], base, lang)
    for st in soup.find_all('style'):
        if st.string: st.string = st.string.replace('url(assets/', 'url(/assets/')
    # <html>, head
    soup.html['lang'] = lang
    head = soup.head
    for c in head.find_all('link', rel='canonical'): c.decompose()
    for m in head.find_all('meta'):
        if m.get('property') == 'og:locale': m['content'] = L['locale']
        if m.get('property') == 'og:url': m['content'] = '%s/%s%s' % (SITE, lang, base)
    head.append(BeautifulSoup('<link rel="canonical" href="%s/%s%s">' % (SITE, lang, base) + hreflang_block(base), 'html.parser'))
    if lang == 'hy':
        head.append(BeautifulSoup('<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Noto+Sans+Armenian:wght@400;600;800&display=swap">'
                                  "<style>html[lang=hy] *{font-family:'Noto Sans Armenian',Manrope,Arial,sans-serif}</style>", 'html.parser'))
    head.append(BeautifulSoup('<style>html:not([lang=ru]) header .nav ul{gap:clamp(8px,1.1vw,18px)}html:not([lang=ru]) header .nav ul a{font-size:clamp(12px,1.05vw,14px)}html:not([lang=ru]) body{overflow-wrap:break-word}</style>', 'html.parser'))
    for s in soup.find_all('script', type='application/ld+json'):
        try: s.string = json.dumps(translate_json(json.loads(s.string), tr, lang, L), ensure_ascii=False)
        except Exception: pass
    # скрипт скрытия кнопок прошедших мероприятий
    for s in soup.find_all('script'):
        if s.string and 'Мероприятия: после даты' in s.string:
            s.string = ("(function(){var p=new Intl.DateTimeFormat('en-CA',{timeZone:'Europe/Moscow',year:'numeric',month:'2-digit',day:'2-digit'}).format(new Date()).split('-');"
                        "var today=Date.UTC(+p[0],+p[1]-1,+p[2]),DAY=864e5;document.querySelectorAll('.ev').forEach(function(c){var pill=c.querySelector('.pill.a'),btn=c.querySelector('.btn');"
                        "if(!pill||!btn||!pill.dataset.d)return;var a=pill.dataset.d.split('-'),y=+p[0],d=Date.UTC(y,+a[0]-1,+a[1]);"
                        "if(today-d>200*DAY)d=Date.UTC(y+1,+a[0]-1,+a[1]);else if(d-today>200*DAY)d=Date.UTC(y-1,+a[0]-1,+a[1]);if(d<today)btn.remove();});})();")
    return str(soup)

def patch_ru(src, base):
    path = os.path.join(ROOT, src)
    html = open(path, encoding='utf-8').read()
    block = hreflang_block(base)
    if HREFLANG in html:
        html = re.sub(re.escape(HREFLANG) + r'.*?<!--/hreflang-->', lambda m: block, html, flags=re.S)
    else:
        html = html.replace('</head>', block + '</head>', 1)
    open(path, 'w', encoding='utf-8').write(html)

def write_sitemap():
    urls = [('/', '1.0', 'weekly'), ('/school/', '0.9', 'weekly'), ('/products/', '0.8', 'weekly'), ('/breakfast/', '0.6', 'weekly'), ('/breakfast-spb/', '0.6', 'weekly')]
    out = ['<?xml version="1.0" encoding="UTF-8"?>',
           '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" xmlns:xhtml="http://www.w3.org/1999/xhtml">']
    import datetime
    today = datetime.date.today().isoformat()
    for path, pr, cf in urls:
        langs = path in PAGE_URLS
        locs = [('', path)] + ([('/' + l, path) for l in LANGS] if langs else [])
        for pre, p in locs:
            out.append('  <url><loc>%s%s%s</loc><lastmod>%s</lastmod><changefreq>%s</changefreq><priority>%s</priority>' % (SITE, pre, p, today, cf, pr))
            if langs:
                out.append('    <xhtml:link rel="alternate" hreflang="ru" href="%s%s"/>' % (SITE, p))
                for l in LANGS: out.append('    <xhtml:link rel="alternate" hreflang="%s" href="%s/%s%s"/>' % (l, SITE, l, p))
                out.append('    <xhtml:link rel="alternate" hreflang="x-default" href="%s%s"/>' % (SITE, p))
            out.append('  </url>')
    out.append('</urlset>')
    open(os.path.join(ROOT, 'sitemap.xml'), 'w', encoding='utf-8').write('\n'.join(out) + '\n')

def main():
    keys = json.load(open(os.path.join(ROOT, 'i18n', 'keys.json'), encoding='utf-8')) if os.path.exists(os.path.join(ROOT, 'i18n', 'keys.json')) else None
    if keys is None: keys = extract_keys([p for p, _ in PAGES])
    for lang in LANGS:
        tr = load_dict(lang, keys)
        for src, base in PAGES:
            out = build_page(src, base, lang, tr)
            d = os.path.join(ROOT, lang, base.strip('/'))
            os.makedirs(d, exist_ok=True)
            open(os.path.join(d, 'index.html'), 'w', encoding='utf-8').write(out)
    for src, base in PAGES: patch_ru(src, base)
    write_sitemap()
    print('ok')

if __name__ == '__main__':
    main()
