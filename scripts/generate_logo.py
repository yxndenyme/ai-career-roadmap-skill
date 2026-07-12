#!/usr/bin/env python3
"""使用 Pillow 生成与矢量标志一致的商店 PNG 图标。"""

from pathlib import Path

from PIL import Image, ImageDraw


ROOT = Path(__file__).resolve().parents[1]
ASSETS = ROOT / "assets"


def interpolate(a: tuple[int, int, int], b: tuple[int, int, int], t: float):
    return tuple(round(x + (y - x) * t) for x, y in zip(a, b))


def create_logo(size: int, output: Path) -> None:
    scale = size / 512
    image = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    pixels = image.load()
    start = (6, 26, 64)
    end = (11, 95, 255)
    for y in range(size):
        for x in range(size):
            t = (x + y) / max(1, 2 * (size - 1))
            pixels[x, y] = (*interpolate(start, end, t), 255)

    mask = Image.new("L", (size, size), 0)
    mask_draw = ImageDraw.Draw(mask)
    inset = round(24 * scale)
    radius = round(112 * scale)
    mask_draw.rounded_rectangle((inset, inset, size - inset, size - inset), radius=radius, fill=255)
    image.putalpha(mask)

    draw = ImageDraw.Draw(image)
    route = [
        (105, 389), (139, 371), (159, 319), (209, 294),
        (257, 278), (278, 232), (314, 211), (355, 190), (394, 126),
    ]
    route = [(round(x * scale), round(y * scale)) for x, y in route]
    draw.line(route, fill=(77, 226, 197, 255), width=round(30 * scale), joint="curve")

    for x, y, color in [
        (106, 389, (77, 226, 197, 255)),
        (210, 294, (99, 231, 181, 255)),
        (315, 211, (156, 245, 138, 255)),
    ]:
        cx, cy = round(x * scale), round(y * scale)
        outer = round(30 * scale)
        inner = round(18 * scale)
        draw.ellipse((cx - outer, cy - outer, cx + outer, cy + outer), fill=color)
        draw.ellipse((cx - inner, cy - inner, cx + inner, cy + inner), fill=(247, 251, 255, 255))

    star = [(398, 85), (410, 117), (442, 129), (410, 141), (398, 173),
            (386, 141), (354, 129), (386, 117)]
    draw.polygon([(round(x * scale), round(y * scale)) for x, y in star], fill=(199, 255, 94, 255))

    output.parent.mkdir(parents=True, exist_ok=True)
    image.save(output, "PNG", optimize=True)


if __name__ == "__main__":
    create_logo(512, ASSETS / "logo.png")
    create_logo(256, ASSETS / "icon.png")
    print("已生成 assets/logo.png 和 assets/icon.png")
