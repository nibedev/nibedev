"""Export transparent GitHub profile graphics for desktop and mobile themes.

Requires Pillow and Microsoft Edge on Windows. Run from any directory:
    python scripts/render_profile_assets.py
"""

from pathlib import Path
import shutil
import subprocess
import time

from PIL import Image


ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "scripts" / "profile_assets.html"
MOBILE_SOURCE = ROOT / "scripts" / "profile_assets_mobile.html"
EDGE = Path(r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe")
SCALE = 2
WINDOW = (1020, 743)
MOBILE_WINDOW = (320, 900)

REGIONS = {
    "intro.png": (0, 0, 660, 260),
    "features.png": (0, 270, 1000, 415),
    "technologies.png": (0, 425, 1020, 543),
    "portfolio-button.png": (0, 553, 500, 643),
    "linkedin-button.png": (0, 643, 500, 733),
    "dribbble-button.png": (560, 553, 785, 643),
    "behance-button.png": (560, 643, 785, 733),
    "button-divider-top.png": (500, 553, 560, 643),
    "button-divider-bottom.png": (500, 643, 560, 733),
}
MOBILE_REGIONS = {
    "intro": (0, 0, 320, 220),
    "features": (0, 230, 320, 494),
    "technologies": (0, 505, 320, 705),
    "portfolio-button": (0, 715, 155, 805),
    "dribbble-button": (165, 715, 320, 805),
    "linkedin-button": (0, 805, 155, 895),
    "behance-button": (165, 805, 320, 895),
}


def safe_remove(path):
    resolved = path.resolve()
    if not resolved.is_relative_to(ROOT):
        raise RuntimeError(f"Refusing to remove a path outside the repository: {resolved}")
    if resolved.is_dir():
        shutil.rmtree(resolved)
    elif resolved.exists():
        resolved.unlink()


def render_theme(theme, mobile=False):
    variant = f"{theme}-mobile" if mobile else theme
    screenshot = ROOT / "scripts" / f".profile-assets-screenshot-{variant}.png"
    edge_profile = ROOT / "scripts" / f".edge-render-profile-{variant}"
    if screenshot.exists():
        safe_remove(screenshot)

    source = MOBILE_SOURCE if mobile else SOURCE
    window = MOBILE_WINDOW if mobile else WINDOW
    regions = MOBILE_REGIONS if mobile else REGIONS
    url = source.as_uri()
    if theme == "light":
        url += "?theme=light"

    command = [
        str(EDGE),
        "--headless=new",
        "--disable-gpu",
        "--disable-extensions",
        "--hide-scrollbars",
        "--default-background-color=00000000",
        "--allow-file-access-from-files",
        "--run-all-compositor-stages-before-draw",
        "--virtual-time-budget=2500",
        f"--user-data-dir={edge_profile}",
        f"--window-size={window[0]},{window[1]}",
        f"--force-device-scale-factor={SCALE}",
        f"--screenshot={screenshot}",
        url,
    ]
    try:
        subprocess.run(command, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, timeout=45)
        deadline = time.monotonic() + 20
        while not screenshot.exists() and time.monotonic() < deadline:
            time.sleep(0.2)
        if not screenshot.exists():
            raise RuntimeError(f"Edge did not create the {variant} screenshot")

        with Image.open(screenshot) as source_image:
            shot = source_image.convert("RGBA")
        if shot.width < window[0] * SCALE or shot.height < window[1] * SCALE:
            raise RuntimeError(f"Unexpected screenshot size: {shot.size}")

        for name, region in regions.items():
            box = tuple(value * SCALE for value in region)
            if mobile:
                output_name = f"{name}-mobile{'-light' if theme == 'light' else ''}.png"
            else:
                output_name = name if theme == "dark" else name.replace(".png", "-light.png")
            output = ROOT / "assets" / output_name
            shot.crop(box).save(output, optimize=True)
            print(f"{output_name}: {output.stat().st_size:,} bytes")
    finally:
        if screenshot.exists():
            safe_remove(screenshot)
        if edge_profile.exists():
            try:
                safe_remove(edge_profile)
            except PermissionError:
                print(f"Edge still uses temporary files in {edge_profile}; remove them after it closes.")


def main():
    if not EDGE.exists():
        raise RuntimeError(f"Microsoft Edge not found at {EDGE}")
    for mobile in (False, True):
        for theme in ("dark", "light"):
            render_theme(theme, mobile=mobile)
    divider = ROOT / "assets" / "button-divider-mobile.png"
    Image.new("RGBA", (10 * SCALE, 90 * SCALE), (0, 0, 0, 0)).save(divider, optimize=True)
    print(f"{divider.name}: {divider.stat().st_size:,} bytes")


if __name__ == "__main__":
    main()
