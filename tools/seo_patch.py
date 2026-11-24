# -*- coding: utf-8 -*-
"""Одноразовый (идемпотентный) патч русских страниц: SEO/GEO-разметка, FAQ, расширенная schema.org."""
import re, json, os
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SITE = 'https://aim-interims.ru'

FAQ = [
 ("Что такое интерим-менеджмент?",
  "Интерим-менеджмент — это временное управление бизнесом или направлением опытным топ-менеджером (CEO, CFO, COO, директор завода и т. д.), который заходит в компанию под конкретную задачу, отвечает за результат и после решения задачи передаёт дела преемнику. Это не консалтинг: интерим сам управляет и внедряет изменения."),
 ("Чем интерим-менеджер отличается от штатного директора и консультанта?",
  "Штатного директора ищут 3–6 месяцев, и с ним сложно и дорого расставаться. Консультант пишет рекомендации и уходит после отчёта. Интерим-менеджер АИМ выходит на проект за 72 часа, сам внедряет изменения, отвечает за результат по KPI и уходит после передачи дел преемнику."),
 ("Как быстро интерим-менеджер выходит на проект?",
  "Ассоциация Интерим Менеджеров предлагает 2–3 кандидатов из пула АИМ в течение 72 часов после первого разговора. Выход на проект — как правило, через 2–4 недели с момента запроса."),
 ("В каких ситуациях бизнесу нужен интерим-менеджер?",
  "Кризис бизнеса, кризис роста, операционный кризис, переезд завода, строительство с нуля, интеграция купленного актива, подготовка к продаже бизнеса, внедрение ERP, выход на новые рынки, внезапный уход топ-менеджера."),
 ("Как устроены ответственность и оплата?",
  "Цели, сроки и KPI фиксируются в интерим-контракте до старта проекта. Интерим отвечает за результат, а не за процесс, и не заинтересован в том, чтобы удерживаться на позиции дольше, чем нужно. Условия обсуждаются на 30-минутном разговоре с партнёром АИМ."),
 ("Сколько длится интерим-проект?",
  "Как правило, до 12 месяцев: интерим решает задачу, готовит преемника и передаёт дела."),
 ("Кто стоит за Ассоциацией Интерим Менеджеров?",
  "Основатель и управляющий партнёр АИМ — Андрей Фомин: 22 года в топ-менеджменте международных корпораций (Magna, Visteon, Motherson, Boge), интерим-проекты в России, Словакии, Германии и Сербии. Он также основал Школу интерим-менеджеров."),
 ("Как стать интерим-менеджером?",
  "Для топ-менеджеров с опытом от 15 лет АИМ проводит Школу интерим-менеджеров: 7 недель, 14 живых онлайн-встреч с практиками, защита собственного кейса, сертификат и доступ к закрытому пулу проектов Ассоциации. Ближайший поток стартует 1 февраля 2027 года. Можно также пройти бесплатный тест «Готов ли я стать интеримом»."),
]

def esc(s): return s.replace('&','&amp;').replace('<','&lt;').replace('>','&gt;')

FAQ_CSS = ("<style>.faq{margin-top:28px;display:grid;gap:12px}.faq details{background:var(--surface);border-radius:16px;padding:0 22px}"
           ".faq summary{cursor:pointer;list-style:none;padding:20px 0;font-weight:800;font-size:18px;display:flex;justify-content:space-between;gap:16px;align-items:center}"
           ".faq summary::-webkit-details-marker{display:none}.faq summary:after{content:'+';color:var(--accent);font-size:26px;line-height:1}"
           ".faq details[open] summary:after{content:'–'}.faq details p{padding:0 0 22px;color:var(--muted)}</style>")
def faq_section():
    items = ''.join('<details><summary>%s</summary><p>%s</p></details>' % (esc(q), esc(a)) for q, a in FAQ)
    return ('<section id="faq">\n  <div class="wrap">\n    <div class="eyebrow">Вопросы и ответы</div>\n    <h2>Частые вопросы об интерим-менеджменте</h2>\n'
            '    <div class="faq">%s</div>\n  </div>\n</section>\n' % items)

def get_ld(html):
    m = re.search(r'<script type="application/ld\+json">(.*?)</script>', html, re.S)
    return m, (json.loads(m.group(1)) if m else None)
def put_ld(html, m, data):
    s = '<script type="application/ld+json">%s</script>' % json.dumps(data, ensure_ascii=False)
    return html[:m.start()] + s + html[m.end():]

def meta_block(html, url):
    og_t = re.search(r'<meta property="og:title" content="([^"]*)"', html)
    og_d = re.search(r'<meta property="og:description" content="([^"]*)"', html)
    parts = ['<!--seo-->']
    if not og_t:
        t = re.search(r'<title>([^<]*)', html); dsc = re.search(r'<meta name="description" content="([^"]*)"', html)
        class _M:  # подставка с group(1)
            def __init__(s, v): s.v = v
            def group(s, i): return s.v
        if t: og_t = _M(t.group(1)); parts.append('<meta property="og:title" content="%s">' % t.group(1))
        if dsc: og_d = _M(dsc.group(1)); parts.append('<meta property="og:description" content="%s">' % dsc.group(1))
        parts.append('<meta property="og:type" content="website"><meta property="og:url" content="%s"><meta property="og:image" content="%s/assets/og.jpg"><meta property="og:locale" content="ru_RU">' % (url, SITE))
    if 'name="robots"' not in html: parts.append('<meta name="robots" content="index,follow,max-image-preview:large,max-snippet:-1,max-video-preview:-1">')
    parts.append('<meta name="theme-color" content="#232325">')
    parts.append('<meta name="twitter:card" content="summary_large_image">')
    if og_t: parts.append('<meta name="twitter:title" content="%s">' % og_t.group(1))
    if og_d: parts.append('<meta name="twitter:description" content="%s">' % og_d.group(1))
    parts.append('<meta name="twitter:image" content="%s/assets/og.jpg">' % SITE)
    parts.append('<meta property="og:image:width" content="1200"><meta property="og:image:height" content="630">')
    parts.append('<meta property="og:image:alt" content="Ассоциация Интерим Менеджеров (АИМ)">')
    parts.append('<!--/seo-->')
    return ''.join(parts)

def apply_meta(html, url):
    html = re.sub(r'<!--seo-->.*?<!--/seo-->', '', html, flags=re.S)
    return html.replace('</head>', meta_block(html, url) + '</head>', 1)

def bc(items):
    return {"@type": "BreadcrumbList", "itemListElement": [{"@type": "ListItem", "position": i+1, "name": n, "item": u} for i, (n, u) in enumerate(items)]}

def patch_index():
    p = os.path.join(ROOT, 'index.html'); html = open(p, encoding='utf-8').read()
    html = re.sub(r'<section id="faq">.*?</section>\n', '', html, flags=re.S)
    html = html.replace('<section id="contacts"', faq_section() + '<section id="contacts"', 1)
    if '.faq{' not in html: html = html.replace('</head>', FAQ_CSS + '</head>', 1)
    m, d = get_ld(html)
    g = [n for n in d['@graph'] if n.get('@type') not in ('FAQPage', 'Service')]
    for n in g:
        if n.get('@type') == 'Organization':
            n['description'] = 'Ассоциация Интерим Менеджеров (АИМ) — сообщество опытных топ-менеджеров для интерим-проектов: подбор интерим-менеджера (CEO, CFO, COO, директор завода) за 72 часа и Школа интерим-менеджеров.'
            n['knowsAbout'] = ['интерим-менеджмент', 'антикризисное управление', 'временное управление бизнесом', 'интерим CEO', 'интерим CFO', 'интерим COO', 'подбор топ-менеджеров', 'релокация производства', 'внедрение ERP', 'подготовка бизнеса к продаже']
            n['areaServed'] = ['RU', 'KZ', 'UZ', 'AM', 'AZ', 'Europe']
            n['contactPoint'] = {"@type": "ContactPoint", "contactType": "sales", "telephone": "+7 911 971 15 19", "email": "af@aiminterims.ru", "availableLanguage": ["ru", "en"], "url": "https://t.me/AndreyAFomin"}
    g.append({"@type": "Service", "@id": SITE + "/#service", "name": "Интерим-менеджмент", "serviceType": "Интерим-менеджмент (временное управление бизнесом топ-менеджером)",
              "provider": {"@id": SITE + "/#org"}, "areaServed": ["RU", "Europe"], "audience": {"@type": "BusinessAudience", "audienceType": "Собственники бизнеса"},
              "description": "Подбор опытного интерим-менеджера из пула АИМ за 72 часа под конкретную задачу бизнеса: кризис, рост, релокация, интеграция активов, внедрение ERP, подготовка к продаже."})
    g.append({"@type": "FAQPage", "@id": SITE + "/#faq", "mainEntity": [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in FAQ]})
    d['@graph'] = g
    html = put_ld(html, m, d)
    html = apply_meta(html, SITE + '/')
    open(p, 'w', encoding='utf-8').write(html)

def patch_school():
    p = os.path.join(ROOT, 'school/index.html'); html = open(p, encoding='utf-8').read()
    m, d = get_ld(html)
    if '@graph' not in d:
        d['@context'] = d.get('@context', 'https://schema.org')
        nodes = [d]; ctx = d.pop('@context'); d = {'@context': ctx, '@graph': nodes}
    g = [n for n in d['@graph'] if n.get('@type') != 'BreadcrumbList']
    for n in g:
        if n.get('@type') == 'Course':
            n['courseMode'] = 'online'; n['educationalCredentialAwarded'] = 'Сертификат Ассоциации Интерим Менеджеров'
            n['audience'] = {"@type": "Audience", "audienceType": "Топ-менеджеры с опытом 15+ лет"}
            n['instructor'] = {"@type": "Person", "name": "Андрей Фомин", "url": "https://t.me/AndreyAFomin"}
            n['url'] = SITE + '/school/'
            ci = n.get('hasCourseInstance', {})
            ci['courseMode'] = 'online'; ci['endDate'] = '2027-03-21'
            n['hasCourseInstance'] = ci
    g.append(bc([('АИМ', SITE + '/'), ('Школа интерим-менеджеров', SITE + '/school/')]))
    d['@graph'] = g
    html = put_ld(html, m, d)
    html = apply_meta(html, SITE + '/school/')
    open(p, 'w', encoding='utf-8').write(html)

PRODUCTS = [("Школа интерим-менеджеров", "7 недель, 14 живых онлайн-встреч, защита собственного кейса, сертификат и доступ к закрытому пулу АИМ.", "400000"),
            ("Персональная консультация: интерим-менеджер как следующий шаг в карьере", "Определение экспертности, разбор резюме и план обеспечения проектами.", "40000"),
            ("Расшифровка теста «Готов ли я стать интеримом»", "Подробная расшифровка результатов по 10 блокам, вердикт о готовности и рекомендации.", "10000"),
            ("Личное менторство собственника бизнеса или руководителя (час)", "Систематизация бизнеса, поиск резервов прибыли, приоритеты и стратегия. Программа из 10 встреч.", "100000")]
def patch_products():
    p = os.path.join(ROOT, 'products/index.html'); html = open(p, encoding='utf-8').read()
    html = re.sub(r'<script type="application/ld\+json">.*?</script>', '', html, flags=re.S)
    d = {"@context": "https://schema.org", "@graph": [
        bc([('АИМ', SITE + '/'), ('Продукты АИМ', SITE + '/products/')]),
        {"@type": "ItemList", "name": "Продукты Ассоциации Интерим Менеджеров", "itemListElement": [
            {"@type": "ListItem", "position": i+1, "item": {"@type": "Product", "name": n, "description": ds, "brand": {"@type": "Organization", "name": "Ассоциация Интерим Менеджеров"},
             "offers": {"@type": "Offer", "price": pr, "priceCurrency": "RUB", "availability": "https://schema.org/InStock", "url": SITE + "/products/"}}}
            for i, (n, ds, pr) in enumerate(PRODUCTS)]}]}
    html = html.replace('</head>', '<script type="application/ld+json">%s</script></head>' % json.dumps(d, ensure_ascii=False), 1)
    if '<link rel="canonical"' not in html: html = html.replace('</head>', '<link rel="canonical" href="%s/products/"></head>' % SITE, 1)
    html = apply_meta(html, SITE + '/products/')
    open(p, 'w', encoding='utf-8').write(html)

if __name__ == '__main__':
    patch_index(); patch_school(); patch_products(); print('seo ok')
