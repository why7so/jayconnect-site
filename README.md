# jayconnect.net — сайт Jay Connect

Информационный сайт VPN-сервиса **Jay Connect**. Статика без сборки: HTML + CSS +
ванильный JS, никаких зависимостей и npm — папку можно открыть локально двойным
кликом по `index.html` или залить на любой статический хостинг как есть.

```
index.html    — вся страница (первый экран, возможности, подключение, тарифы,
                устройства, вопросы, финальный блок, подвал)
style.css     — оформление; тёмная тема, акцент #52aa52 как в мини-приложении,
                светлым выделен только блок вопросов
assets/jay.png — логотип для og:image и иконки на iOS
main.js       — появление блоков, кольцо подписки, вопросы, меню и липкая
                кнопка на телефонах
favicon.svg   — логотип-сойка
CNAME         — домен для GitHub Pages (jayconnect.net)
robots.txt / sitemap.xml / .nojekyll
```

## Куда что ведёт

| Ссылка на сайте | Куда идёт |
| --- | --- |
| «Начать бесплатно», «Открыть в Telegram» | https://t.me/jayconnectbot |
| «Личный кабинет» | https://app.jayconnect.net (мини-приложение) |
| Поддержка | https://t.me/jayconnect_support |
| Условия и политика | `app.jayconnect.net/terms.html`, `/privacy.html` |

Цены и лимиты на странице продублированы вручную из `config.py` бота
(`PLANS`, `DEVICE_LIMIT`, `EXTRA_DEVICE_PRICE_RUB`, `TRIAL_DAYS`,
`REFERRAL_*`). **При изменении тарифов в боте не забудьте поправить блок
`#pricing` и цифры в герое** — сайт не ходит в API и ничего не подтягивает
динамически.

## Деплой на GitHub Pages

1. Settings → Pages → Source: **Deploy from a branch**, ветка `main`, папка `/ (root)`.
2. Custom domain: `jayconnect.net` (файл `CNAME` уже в репозитории), включить
   **Enforce HTTPS**.
3. У регистратора домена прописать записи:
   - `A` для `@` → `185.199.108.153`, `185.199.109.153`, `185.199.110.153`, `185.199.111.153`
   - `CNAME` для `www` → `<username>.github.io`

`.nojekyll` отключает обработку Jekyll — файлы отдаются ровно такими, какие есть.

## Деплой на Vercel / Netlify

Импортировать репозиторий, Framework Preset — **Other**, build-команда пустая,
publish directory — корень (`.`). Домен `jayconnect.net` добавляется в настройках
проекта.

## Локальный просмотр

```bash
python -m http.server 8000
```

Затем открыть http://localhost:8000. Отдельный сервер нужен только для
корректных путей — сам сайт работает и из файловой системы.
