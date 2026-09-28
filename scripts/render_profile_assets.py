"""Export transparent GitHub profile graphics for dark and light themes.

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
EDGE = Path(r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe")
SCALE = 2
WINDOW = (1020, 743)

REGIONS = {
    "intro.png": (0, 0, 660, 260),
    "features.png": (0, 270, 1000, 415),
    "technologies.png": (0, 425, 1020, 543),
    "portfolio-button.png": (0, 553, 570, 643),
    "linkedin-button.png": (0, 643, 570, 733),
    "dribbble-button.png": (645, 553, 870, 643),
    "behance-button.png": (645, 643, 870, 733),
    "button-divider-top.png": (570, 553, 645, 643),
    "button-divider-bottom.png": (570, 643, 645, 733),
}


def safe_remove(path):
    resolved = path.resolve()
    if not resolved.is_relative_to(ROOT):
        raise RuntimeError(f"Refusing to remove a path outside the repository: {resolved}")
    if resolved.is_dir():
        shutil.rmtree(resolved)
    elif resolved.exists():
        resolved.unlink()


def render_theme(theme):
    screenshot = ROOT / "scripts" / f".profile-assets-screenshot-{theme}.png"
    edge_profile = ROOT / "scripts" / f".edge-render-profile-{theme}"
    if screenshot.exists():
        safe_remove(screenshot)

    url = SOURCE.as_uri()
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
        f"--window-size={WINDOW[0]},{WINDOW[1]}",
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
            raise RuntimeError(f"Edge did not create the {theme} screenshot")

        with Image.open(screenshot) as source:
            shot = source.convert("RGBA")
        if shot.width < WINDOW[0] * SCALE or shot.height < WINDOW[1] * SCALE:
            raise RuntimeError(f"Unexpected screenshot size: {shot.size}")

        for name, region in REGIONS.items():
            box = tuple(value * SCALE for value in region)
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
    for theme in ("dark", "light"):
        render_theme(theme)


if __name__ == "__main__":
    main()
