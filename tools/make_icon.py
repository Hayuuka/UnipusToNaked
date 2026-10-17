# -*- coding: utf-8 -*-
"""生成应用图标 icon.ico（可重复运行）。"""

from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

SIZE = 512
ROOT = Path(__file__).resolve().parent.parent


def rounded_gradient(size: int) -> Image.Image:
    img = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    grad = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    px = grad.load()
    top = (59, 130, 246)      # #3B82F6
    bottom = (29, 78, 216)    # #1D4ED8
    for y in range(size):
        t = y / (size - 1)
        color = tuple(round(top[i] * (1 - t) + bottom[i] * t) for i in range(3)) + (255,)
        for x in range(size):
            px[x, y] = color
    mask = Image.new("L", (size, size), 0)
    ImageDraw.Draw(mask).rounded_rectangle((12, 12, size - 12, size - 12), radius=112, fill=255)
    img.paste(grad, (0, 0), mask)
    return img


def main() -> None:
    img = rounded_gradient(SIZE)
    d = ImageDraw.Draw(img)

    font_path = Path(r"C:\Windows\Fonts\segoeuib.ttf")
    if not font_path.exists():
        font_path = Path(r"C:\Windows\Fonts\arialbd.ttf")
    font = ImageFont.truetype(str(font_path), 310)

    # 字母 U
    text = "U"
    box = d.textbbox((0, 0), text, font=font)
    tw, th = box[2] - box[0], box[3] - box[1]
    d.text((196 - tw / 2 - box[0], 250 - th / 2 - box[1]), text, font=font, fill=(255, 255, 255, 255))

    # 右下角小锁
    lock_x, lock_y = 330, 300
    body = (lock_x, lock_y + 55, lock_x + 130, lock_y + 160)
    d.rounded_rectangle(body, radius=26, fill=(255, 255, 255, 255))
    d.arc((lock_x + 22, lock_y, lock_x + 108, lock_y + 120), 180, 360, fill=(255, 255, 255, 255), width=22)
    # 钥匙孔
    cx = lock_x + 65
    d.ellipse((cx - 15, lock_y + 88, cx + 15, lock_y + 118), fill=(37, 99, 235, 255))
    d.polygon([(cx - 9, lock_y + 108), (cx + 9, lock_y + 108), (cx + 5, lock_y + 146), (cx - 5, lock_y + 146)], fill=(37, 99, 235, 255))

    img.save(ROOT / "icon.png")
    img.save(
        ROOT / "icon.ico",
        sizes=[(16, 16), (24, 24), (32, 32), (48, 48), (64, 64), (128, 128), (256, 256)],
    )
    print("icon.ico / icon.png written")


if __name__ == "__main__":
    main()