# Generate TalkBell banner assets (main 1200x400, event 400x300) in JPG/PNG/GIF/WebP.
from __future__ import annotations

import os
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

OUT = Path(__file__).resolve().parent
FONT_BOLD = Path(os.environ.get("WINDIR", "C:/Windows")) / "Fonts" / "malgunbd.ttf"
FONT_REG = Path(os.environ.get("WINDIR", "C:/Windows")) / "Fonts" / "malgun.ttf"


def load_font(size: int, bold: bool = False) -> ImageFont.FreeTypeFont:
    p = FONT_BOLD if bold else FONT_REG
    if not p.is_file():
        return ImageFont.load_default()
    return ImageFont.truetype(str(p), size)


def horizontal_gradient(size: tuple[int, int], left: tuple[int, int, int], right: tuple[int, int, int]) -> Image.Image:
    w, h = size
    img = Image.new("RGB", size)
    px = img.load()
    for x in range(w):
        t = x / max(w - 1, 1)
        r = int(left[0] * (1 - t) + right[0] * t)
        g = int(left[1] * (1 - t) + right[1] * t)
        b = int(left[2] * (1 - t) + right[2] * t)
        for y in range(h):
            px[x, y] = (r, g, b)
    return img


def add_soft_vignette(base: Image.Image, strength: float = 0.12) -> Image.Image:
    w, h = base.size
    overlay = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    d = ImageDraw.Draw(overlay)
    cx, cy = w * 0.5, h * 0.45
    max_r = (w * w + h * h) ** 0.5 * 0.55
    for i in range(40, 0, -1):
        alpha = int(255 * strength * (i / 40) ** 2)
        d.ellipse(
            [cx - max_r * i / 40, cy - max_r * i / 40, cx + max_r * i / 40, cy + max_r * i / 40],
            outline=(0, 0, 0, alpha),
            width=max(2, w // 200),
        )
    return Image.alpha_composite(base.convert("RGBA"), overlay).convert("RGB")


def draw_main_banner() -> Image.Image:
    w, h = 1200, 400
    # Mint → brand green (matches landing --primary-accent #5CB85C family)
    left = (236, 252, 240)
    right = (46, 140, 80)
    img = horizontal_gradient((w, h), left, right)
    img = add_soft_vignette(img, 0.08)
    d = ImageDraw.Draw(img)
    f_title = load_font(56, bold=True)
    f_sub = load_font(26, bold=False)
    f_line = load_font(22, bold=False)
    f_badge = load_font(18, bold=True)

    # Left-aligned copy
    x0, y0 = 64, 88
    d.text((x0, y0), "문자 · LMS/MMS · 알림톡 · 브랜드메시지", fill=(38, 95, 58), font=f_sub)
    d.text((x0, y0 + 44), "합리적 단가로 빠르게 발송하세요", fill=(40, 90, 55), font=f_title)
    d.text((x0, y0 + 128), "톡벨 TalkBell — 비즈니스 메시징", fill=(30, 70, 45), font=f_line)

    # Accent pill (orange #FF6B35)
    bx, by = x0, y0 + 178
    pill = "지금 시작하기"
    bbox = d.textbbox((0, 0), pill, font=f_badge)
    pw = bbox[2] - bbox[0] + 36
    ph = bbox[3] - bbox[1] + 20
    d.rounded_rectangle([bx, by, bx + pw, by + ph], radius=10, fill=(255, 107, 53))
    d.text((bx + 18, by + 10), pill, fill=(255, 255, 255), font=f_badge)

    # Decorative circles (right)
    for i, (cx, cy, r, fill) in enumerate(
        [
            (1020, 120, 140, (255, 255, 255, 35)),
            (1080, 260, 90, (255, 255, 255, 25)),
            (980, 280, 55, (255, 255, 255, 30)),
        ]
    ):
        layer = Image.new("RGBA", (w, h), (0, 0, 0, 0))
        ld = ImageDraw.Draw(layer)
        ld.ellipse([cx - r, cy - r, cx + r, cy + r], fill=fill)
        img = Image.alpha_composite(img.convert("RGBA"), layer).convert("RGB")
        d = ImageDraw.Draw(img)

    return img


def draw_event_banner() -> Image.Image:
    w, h = 400, 300
    left = (255, 248, 240)
    right = (46, 130, 75)
    img = horizontal_gradient((w, h), left, right)
    d = ImageDraw.Draw(img)
    f1 = load_font(28, bold=True)
    f2 = load_font(17, bold=False)
    f3 = load_font(15, bold=False)
    d.text((28, 36), "이벤트", fill=(32, 85, 52), font=f1)
    d.text((28, 82), "충전 보너스 &", fill=(40, 80, 50), font=f2)
    d.text((28, 108), "특별 요금 확인", fill=(40, 80, 50), font=f2)
    d.text((28, 220), "톡벨 TalkBell", fill=(255, 255, 255), font=f3)
    # small accent bar
    d.rounded_rectangle([28, 160, 120, 168], radius=3, fill=(255, 107, 53))
    return img


def save_all(name_prefix: str, img: Image.Image) -> None:
    jpg_path = OUT / f"{name_prefix}.jpg"
    png_path = OUT / f"{name_prefix}.png"
    gif_path = OUT / f"{name_prefix}.gif"
    webp_path = OUT / f"{name_prefix}.webp"

    rgb = img.convert("RGB")
    rgb.save(jpg_path, "JPEG", quality=90, optimize=True, progressive=True)
    rgb.save(png_path, "PNG", optimize=True)

    # Animated GIF: 2 frames (subtle brightness) — keeps size small
    f1 = rgb
    f2 = Image.eval(rgb, lambda p: min(255, int(p * 1.04)))
    frames = [f1, f2]
    frames[0].save(
        gif_path,
        save_all=True,
        append_images=frames[1:],
        duration=800,
        loop=0,
        optimize=True,
    )

    rgb.save(webp_path, "WEBP", quality=88, method=6)

    for p in (jpg_path, png_path, gif_path, webp_path):
        sz = p.stat().st_size
        ok = "OK" if sz <= 5 * 1024 * 1024 else "OVER 5MB"
        print(f"{p.name}: {sz // 1024} KB — {ok}")


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    main_img = draw_main_banner()
    event_img = draw_event_banner()
    save_all("banner-main-1200x400", main_img)
    save_all("banner-event-400x300", event_img)
    print("Done.")


if __name__ == "__main__":
    main()
