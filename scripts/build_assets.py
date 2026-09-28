"""Build the local visual assets used by the GitHub profile README.

Run from the repository root: python scripts/build_assets.py
Requires Pillow only for the animated cat image.
"""

from __future__ import annotations

import html
import re
from pathlib import Path

from PIL import Image


ROOT = Path(__file__).resolve().parents[1]
ASSETS = ROOT / "assets"
VENDOR = ASSETS / "vendor"
SOURCE_GIF = ROOT / "3_Gato_acostado_FINAL.gif"

WHITE = "#e6eaf2"
MUTED = "#9aa7bd"
YELLOW = "#f5d547"
FONT = "Segoe UI, Arial, sans-serif"


def svg_document(width: int, height: int, contents: str) -> str:
    return (
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" '
        f'viewBox="0 0 {width} {height}" role="img">'
        f'<rect width="{width}" height="{height}" fill="#0d1117"/>'
        f"{contents}</svg>\n"
    )


def embedded_icon(name: str, x: int, y: int, size: int, *, color: str | None = None) -> str:
    source = (VENDOR / f"{name}.svg").read_text(encoding="utf-8")
    match = re.search(r"<svg\b[^>]*\bviewBox=[\"']([^\"']+)[\"'][^>]*>", source, re.S)
    if not match:
        raise ValueError(f"Missing SVG viewBox: {name}")
    body = source[match.end() : source.rfind("</svg>")]
    # Brand SVGs can reuse gradient IDs; prefix each ID before composing one image.
    body = re.sub(r'\bid="([^"]+)"', lambda m: f'id="{name}-{m.group(1)}"', body)
    body = re.sub(r'url\(#([^)]+)\)', lambda m: f'url(#{name}-{m.group(1)})', body)
    body = re.sub(r'href="#([^"]+)"', lambda m: f'href="#{name}-{m.group(1)}"', body)
    if color and not name.startswith("lucide-"):
        body = body.replace("currentColor", color)
        body = re.sub(r'<path\b(?![^>]*\bfill=)', f'<path fill="{color}"', body)
    line_style = (
        f' fill="none" stroke="{color}" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"'
        if name.startswith("lucide-") else ""
    )
    return (
        f'<svg x="{x}" y="{y}" width="{size}" height="{size}" '
        f'viewBox="{match.group(1)}"{line_style}>{body}</svg>'
    )


def build_intro() -> None:
    content = f"""
      <text x="10" y="42" fill="{MUTED}" font-family="{FONT}" font-size="23" font-weight="600">Hello, I’m nibe</text>
      <text x="10" y="101" fill="{WHITE}" font-family="{FONT}" font-size="42" font-weight="700">A front-end developer</text>
      <text x="10" y="150" fill="{WHITE}" font-family="{FONT}" font-size="35" font-weight="700"><tspan>who loves </tspan><tspan fill="{YELLOW}">design</tspan><tspan> and </tspan><tspan fill="{YELLOW}">videogames.</tspan></text>
      <path d="M11 183v50" stroke="#a5afc0" stroke-width="2"/>
      <text x="29" y="200" fill="{MUTED}" font-family="{FONT}" font-size="17.5">I create accessible and delightful web experiences,</text>
      <text x="29" y="225" fill="{MUTED}" font-family="{FONT}" font-size="17.5">turning ideas into beautiful, functional interfaces.</text>
    """
    (ASSETS / "intro.svg").write_text(svg_document(660, 250, content), encoding="utf-8")


def build_features() -> None:
    items = [
        ("lucide-monitor", "#d58aff", ("Front-End", "Development"), ("Vue · JavaScript", "Modern CSS")),
        ("lucide-box", "#f2bd65", ("Design Systems", "& UI/UX"), ("Interfaces", "that scale")),
        ("lucide-pencil", "#8388ff", ("From Figma", "to Production"), ("Design to code", "with attention to detail")),
        ("lucide-gamepad-2", "#e297f4", ("Open to", "new challenges"), ("Always learning", "and building")),
    ]
    chunks = []
    for index, (icon, color, heading, subline) in enumerate(items):
        x = index * 250 + 10
        chunks.append(embedded_icon(icon, x + 8, 14, 43, color=color))
        for line, offset in zip(heading, (29, 56)):
            chunks.append(f'<text x="{x+66}" y="{offset}" fill="{WHITE}" font-family="{FONT}" font-size="17" font-weight="700">{html.escape(line)}</text>')
        for line, offset in zip(subline, (96, 123)):
            chunks.append(f'<text x="{x+66}" y="{offset}" fill="{MUTED if index else "#69bbf1"}" font-family="{FONT}" font-size="16">{html.escape(line)}</text>')
    (ASSETS / "features.svg").write_text(svg_document(1000, 145, "".join(chunks)), encoding="utf-8")


def build_technologies() -> None:
    items = [
        ("HTML", "html5"),
        ("CSS", "css3"),
        ("JavaScript", "javascript"),
        ("Vue", "vuejs"),
        ("Vite", "vitejs"),
        ("Git", "git"),
        ("Figma", "figma"),
        ("Photoshop", "photoshop"),
        ("Illustrator", "illustrator"),
        ("AutoCAD", "autocad"),
    ]
    chunks = []
    for i, (label, icon) in enumerate(items):
        x = 5 + i * 99 + (12 if i >= 6 else 0)
        chunks.append(f'<rect x="{x+8}" y="5" width="72" height="72" rx="12" fill="#2B303A"/>')
        chunks.append(embedded_icon(icon, x + (14 if icon == "autocad" else 20), 11 if icon == "autocad" else 17, 60 if icon == "autocad" else 48))
        chunks.append(f'<text x="{x+44}" y="103" text-anchor="middle" fill="{MUTED}" font-family="{FONT}" font-size="13.5">{html.escape(label)}</text>')
    chunks.append('<path d="M603 9v72" stroke="#394250" stroke-width="1.5"/>')
    (ASSETS / "technologies.svg").write_text(svg_document(1020, 118, "".join(chunks)), encoding="utf-8")


def build_contact() -> None:
    linkedin = f"""
      <defs><linearGradient id="blue" x2="1" y2="1"><stop stop-color="#267ce4"/><stop offset="1" stop-color="#1553bb"/></linearGradient></defs>
      <rect x="0" y="31" width="350" height="50" rx="11" fill="url(#blue)"/>
      <rect x="0" y="31" width="51" height="50" rx="11" fill="#368efa" fill-opacity=".5"/>
      {embedded_icon('linkedin', 12, 42, 28)}
      <text x="64" y="62" fill="#ffffff" font-family="{FONT}" font-size="15" font-weight="700">Let’s connect on LinkedIn</text>
      <path d="M311 56h22m-7-7 7 7-7 7" stroke="#fff" stroke-width="2" fill="none" stroke-linecap="round" stroke-linejoin="round"/>
    """
    (ASSETS / "linkedin-button.svg").write_text(svg_document(350, 90, linkedin), encoding="utf-8")
    socials = [
        ("dribbble", "Dribbble", "#ea4c89", True),
        ("behance", "Behance", "#1769ff", False),
    ]
    for icon, label, color, show_heading in socials:
        heading = (
            f'<text x="0" y="20" fill="{MUTED}" font-family="{FONT}" font-size="14">Other places I share my work</text>'
            if show_heading else ""
        )
        content = f"""
          {heading}
          <rect x="0" y="31" width="225" height="50" rx="10" fill="#1d222d" stroke="#36404e"/>
          {embedded_icon(icon, 15, 43, 25, color=color)}
          <text x="50" y="62" fill="{WHITE}" font-family="{FONT}" font-size="15">{label}</text>
          <path d="M183 58h15m-6-6 6 6-6 6" stroke="{MUTED}" stroke-width="1.7" fill="none" stroke-linecap="round" stroke-linejoin="round"/>
        """
        (ASSETS / f"{icon}-button.svg").write_text(svg_document(225, 90, content), encoding="utf-8")
    (ASSETS / "button-gap.svg").write_text(svg_document(14, 90, ""), encoding="utf-8")


def build_cat() -> None:
    source = Image.open(SOURCE_GIF)
    width = 440
    height = round(source.height * width / source.width)
    frames: list[Image.Image] = []
    durations: list[int] = []
    for index in range(source.n_frames):
        source.seek(index)
        rgba = source.convert("RGBA").resize((width, height), Image.Resampling.LANCZOS)
        alpha = rgba.getchannel("A").point(lambda value: 255 if value > 110 else 0)
        rgb = Image.new("RGB", (width, height), (13, 17, 23))
        rgb.paste(rgba, mask=alpha)
        paletted = rgb.quantize(colors=254, method=Image.Quantize.FASTOCTREE)
        frames.append(paletted)
        durations.append(source.info.get("duration", 40))
    frames[0].save(
        ASSETS / "cat-animated.gif",
        save_all=True,
        append_images=frames[1:],
        duration=durations,
        loop=0,
        disposal=2,
        optimize=True,
    )



def main() -> None:
    ASSETS.mkdir(exist_ok=True)
    build_intro()
    build_features()
    build_technologies()
    build_contact()
    build_cat()


if __name__ == "__main__":
    main()

