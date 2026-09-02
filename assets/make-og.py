"""Генератор картинки-превью (og:image) для jayconnect.net.

Запускать вручную после смены логотипа или подписи:

    python assets/make-og.py

Результат — assets/og.png, 1200x630: столько ждут Telegram, ВКонтакте,
WhatsApp и поисковики.
"""

from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parent
W, H = 1200, 630
BG = (7, 16, 9)          # тот же зелёно-чёрный, что и фон сайта
WHITE = (241, 243, 238)
GREEN = (82, 170, 82)
DIM = (154, 161, 154)

FONT_BOLD = "C:/Windows/Fonts/segoeuib.ttf"
FONT_REG = "C:/Windows/Fonts/segoeui.ttf"


def glow(img: Image.Image) -> None:
    """Мягкое зелёное свечение сверху — как на первом экране сайта.

    Рисуем маленькое пятно и растягиваем: так градиент считается по сотне
    пикселей вместо миллиона, а на глаз результат тот же."""
    small = Image.new("RGB", (60, 32), BG)
    px = small.load()
    cx, cy, r = 30, 2, 34
    for y in range(32):
        for x in range(60):
            d = ((x - cx) ** 2 + (y - cy) ** 2) ** 0.5
            k = max(0.0, 1 - d / r) ** 2 * 0.42
            px[x, y] = tuple(int(BG[i] + (GREEN[i] - BG[i]) * k) for i in range(3))
    img.paste(small.resize((W, H // 2), Image.LANCZOS), (0, 0))


def logo_mark(size: int) -> Image.Image:
    """Сойка с прозрачным фоном.

    В jay.png подложка непрозрачная (#0b0c0b), и на свечении она видна
    тёмным квадратом. Логотип одноцветный, поэтому прозрачность
    восстанавливаем по зелёному каналу: 16 — это фон, 170 — сам знак,
    промежуточные значения дают сглаженные края.
    """
    src = Image.open(ROOT / "jay.png").convert("RGB").resize((size, size), Image.LANCZOS)
    alpha = src.split()[1].point(lambda v: max(0, min(255, round((v - 18) * 255 / 152))))
    flat = Image.new("RGB", src.size, GREEN)
    return Image.merge("RGBA", (*flat.split(), alpha))


def tracked(draw: ImageDraw.ImageDraw, xy, text, font, fill, spacing):
    """Текст с разрядкой: у PIL её нет, поэтому ведём курсор сами."""
    x, y = xy
    for ch in text:
        draw.text((x, y), ch, font=font, fill=fill)
        x += draw.textlength(ch, font=font) + spacing
    return x


def main() -> None:
    img = Image.new("RGB", (W, H), BG)
    glow(img)
    draw = ImageDraw.Draw(img)

    mark = logo_mark(150)
    img.paste(mark, (100, 96), mark)

    word = ImageFont.truetype(FONT_BOLD, 62)
    x = tracked(draw, (268, 140), "JAY ", word, WHITE, 6)
    tracked(draw, (x, 140), "CONNECT", word, GREEN, 6)

    draw.text((100, 300), "VPN с управлением", font=ImageFont.truetype(FONT_BOLD, 76), fill=WHITE)
    draw.text((100, 386), "в Telegram", font=ImageFont.truetype(FONT_BOLD, 76), fill=WHITE)

    draw.line([(100, 512), (1100, 512)], fill=(255, 255, 255, 20), width=1)

    facts = ImageFont.truetype(FONT_REG, 30)
    draw.text((100, 536), "Безлимитный трафик", font=facts, fill=DIM)
    draw.text((445, 536), "3 устройства", font=facts, fill=DIM)
    draw.text((690, 536), "3 дня бесплатно", font=facts, fill=DIM)
    draw.text((972, 536), "от 199 ₽", font=ImageFont.truetype(FONT_BOLD, 30), fill=GREEN)

    out = ROOT / "og.png"
    img.save(out, optimize=True)
    print(f"{out} — {out.stat().st_size // 1024} КБ")


if __name__ == "__main__":
    main()
