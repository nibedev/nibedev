"""Build the local visual assets used by the GitHub profile README.

Run from the repository root: python scripts/build_assets.py
Requires Pillow only for the animated cat and avatar images.
"""

from __future__ import annotations

import html
import re
from pathlib import Path

from PIL import Image, ImageDraw


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
        ("HTML", "html5", "#612016", "#e44d26"),
        ("CSS", "css3", "#0a315e", "#1572b6"),
        ("JavaScript", "javascript", "#504411", "#f7df1e"),
        ("Vue", "vuejs", "#202a38", "#41b883"),
        ("Vite", "vitejs", "#24243a", "#8d56e7"),
        ("Git", "git", "#4a2024", "#f05032"),
        ("Figma", "figma", "#242731", "#ee5f54"),
        ("Photoshop", "photoshop", "#09213a", "#31a8ff"),
        ("Illustrator", "illustrator", "#311908", "#ff9a00"),
        ("AutoCAD", "autocad", "#2a242d", "#e04444"),
    ]
    chunks = [
        '<defs><linearGradient id="tile" x2="1" y2="1"><stop stop-color="#ffffff" stop-opacity=".08"/><stop offset="1" stop-color="#000000" stop-opacity=".12"/></linearGradient></defs>'
    ]
    for i, (label, icon, bg, accent) in enumerate(items):
        x = 5 + i * 99 + (12 if i >= 6 else 0)
        chunks.append(f'<rect x="{x+8}" y="5" width="72" height="72" rx="12" fill="{bg}"/>')
        chunks.append(f'<rect x="{x+8}" y="5" width="72" height="72" rx="12" fill="url(#tile)"/>')
        chunks.append(embedded_icon(icon, x + 20, 17, 48, color=accent if icon == "autocad" else None))
        chunks.append(f'<text x="{x+44}" y="103" text-anchor="middle" fill="{MUTED}" font-family="{FONT}" font-size="13.5">{html.escape(label)}</text>')
    chunks.append('<path d="M603 9v72" stroke="#394250" stroke-width="1.5"/>')
    (ASSETS / "technologies.svg").write_text(svg_document(1020, 118, "".join(chunks)), encoding="utf-8")


def build_contact() -> None:
    linkedin = f"""
      <defs><linearGradient id="blue" x2="1" y2="1"><stop stop-color="#267ce4"/><stop offset="1" stop-color="#1553bb"/></linearGradient></defs>
      <rect x="3" y="8" width="397" height="69" rx="13" fill="url(#blue)"/>
      <rect x="3" y="8" width="71" height="69" rx="13" fill="#368efa" fill-opacity=".5"/>
      {embedded_icon('linkedin', 23, 25, 36)}
      <text x="89" y="51" fill="#ffffff" font-family="{FONT}" font-size="17" font-weight="700">Let’s connect on LinkedIn</text>
      <path d="M357 44h22m-7-7 7 7-7 7" stroke="#fff" stroke-width="2" fill="none" stroke-linecap="round" stroke-linejoin="round"/>
    """
    (ASSETS / "linkedin-button.svg").write_text(svg_document(405, 85, linkedin), encoding="utf-8")
    social = f"""
      <text x="15" y="18" fill="{MUTED}" font-family="{FONT}" font-size="15">Other places I share my work</text>
      <rect x="15" y="32" width="248" height="46" rx="10" fill="#1d222d" stroke="#36404e"/>
      <rect x="281" y="32" width="248" height="46" rx="10" fill="#1d222d" stroke="#36404e"/>
      {embedded_icon('dribbble', 30, 43, 24, color='#ea4c89')}
      {embedded_icon('behance', 296, 43, 24, color='#1769ff')}
      <text x="66" y="61" fill="{WHITE}" font-family="{FONT}" font-size="15">Dribbble</text>
      <text x="332" y="61" fill="{WHITE}" font-family="{FONT}" font-size="15">Behance</text>
      <text x="174" y="61" fill="{MUTED}" font-family="{FONT}" font-size="12">Coming soon</text>
      <text x="438" y="61" fill="{MUTED}" font-family="{FONT}" font-size="12">Coming soon</text>
    """
    (ASSETS / "social-soon.svg").write_text(svg_document(545, 85, social), encoding="utf-8")


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

    # Optional profile avatar: crop the eyes from the original drawing.
    source.seek(0)
    face = source.convert("RGBA").crop((350, 620, 950, 1035))
    face.thumbnail((450, 450), Image.Resampling.LANCZOS)
    avatar = Image.new("RGBA", (512, 512), (0, 0, 0, 255))
    avatar.alpha_composite(face, ((512 - face.width) // 2, (512 - face.height) // 2))
    mask = Image.new("L", (512, 512))
    ImageDraw.Draw(mask).ellipse((8, 8, 503, 503), fill=255)
    avatar.putalpha(mask)
    avatar.save(ASSETS / "avatar.png", optimize=True)


def main() -> None:
    ASSETS.mkdir(exist_ok=True)
    build_intro()
    build_features()
    build_technologies()
    build_contact()
    build_cat()


if __name__ == "__main__":
    main()
