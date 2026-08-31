"""Пересборка микроразметки Schema.org в index.html.

Запускать после правки блока вопросов или цен:

    python assets/make-jsonld.py

Вопросы и ответы берутся из самой страницы, а не пишутся руками: если текст
в разметке разойдётся с текстом на экране, поисковики считают это обманом и
снимают расширенный сниппет. Цены лежат в PRICES ниже — их правим здесь же,
одновременно с блоком #pricing в index.html.
"""

import html
import io
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
PAGE = ROOT / "index.html"
SITE = "https://jayconnect.net/"

PRICES = [("1 месяц", "199"), ("3 месяца", "499"), ("12 месяцев", "1499")]

QA_RE = re.compile(
    r'<button class="qa-q" type="button">(.*?)<i></i></button>\s*'
    r'<div class="qa-a"><div><p>(.*?)</p></div></div>',
    re.S,
)

BLOCK_RE = re.compile(
    r'<!-- Микроразметка Schema\.org.*?</script>\n\n', re.S
)


def plain(fragment: str) -> str:
    """Текст без тегов и лишних пробелов — разметка не любит HTML внутри."""
    return html.unescape(" ".join(re.sub(r"<[^>]+>", "", fragment).split()))


def build(page: str) -> str:
    qa = QA_RE.findall(page)
    if not qa:
        raise SystemExit("не нашёл ни одного вопроса — изменилась разметка FAQ?")

    org = {"@id": SITE + "#organization"}
    graph = [
        {
            "@type": "Organization",
            "@id": org["@id"],
            "name": "Jay Connect",
            "alternateName": ["Джей Коннект", "Jay VPN", "Jay Connect VPN"],
            "url": SITE,
            "logo": {"@type": "ImageObject", "url": SITE + "assets/jay.png", "width": 512, "height": 512},
            "image": SITE + "assets/og.png",
            "description": "VPN-сервис с управлением через Telegram-бот: безлимитный трафик, "
                           "три устройства в подписке, оплата в рублях или USDT.",
            "sameAs": ["https://t.me/jayconnectbot", "https://t.me/jayconnect_support"],
            "contactPoint": [{
                "@type": "ContactPoint",
                "contactType": "customer support",
                "url": "https://t.me/jayconnect_support",
                "availableLanguage": ["Russian"],
            }],
        },
        {
            "@type": "WebSite",
            "@id": SITE + "#website",
            "url": SITE,
            "name": "Jay Connect",
            "inLanguage": "ru-RU",
            "publisher": org,
        },
        {
            "@type": "Product",
            "@id": SITE + "#subscription",
            "name": "Подписка Jay Connect VPN",
            "description": "Доступ к VPN Jay Connect: безлимитный трафик и скорость, три устройства "
                           "по одной ссылке-подписке, протоколы VLESS Reality и Hysteria2, "
                           "управление через Telegram.",
            "image": SITE + "assets/og.png",
            "brand": org,
            "category": "VPN",
            "offers": {
                "@type": "AggregateOffer",
                "priceCurrency": "RUB",
                "lowPrice": PRICES[0][1],
                "highPrice": PRICES[-1][1],
                "offerCount": len(PRICES),
                "availability": "https://schema.org/InStock",
                "url": SITE + "#pricing",
                "offers": [
                    {
                        "@type": "Offer",
                        "name": name,
                        "price": price,
                        "priceCurrency": "RUB",
                        "url": SITE + "#pricing",
                        "availability": "https://schema.org/InStock",
                    }
                    for name, price in PRICES
                ],
            },
        },
        {
            "@type": "FAQPage",
            "@id": SITE + "#faq",
            "isPartOf": {"@id": SITE + "#website"},
            "mainEntity": [
                {
                    "@type": "Question",
                    "name": plain(q),
                    "acceptedAnswer": {"@type": "Answer", "text": plain(a)},
                }
                for q, a in qa
            ],
        },
    ]

    data = json.dumps({"@context": "https://schema.org", "@graph": graph},
                      ensure_ascii=False, indent=2)
    return (
        "<!-- Микроразметка Schema.org. Вопросы и ответы сгенерированы из самого блока\n"
        "     FAQ (assets/make-jsonld.py), поэтому текст на странице и в разметке\n"
        "     совпадает — за расхождение поисковики наказывают. -->\n"
        f"<script type=\"application/ld+json\">\n{data}\n</script>\n\n"
    )


def main() -> None:
    page = io.open(PAGE, encoding="utf-8").read()
    block = build(page)
    if BLOCK_RE.search(page):
        page = BLOCK_RE.sub(lambda _: block, page, count=1)
    else:
        page = page.replace('<script src="main.js', block + '<script src="main.js', 1)
    io.open(PAGE, "w", encoding="utf-8", newline="\n").write(page)
    print(f"разметка обновлена: {len(QA_RE.findall(page))} вопросов, {len(PRICES)} тарифа")


if __name__ == "__main__":
    main()
