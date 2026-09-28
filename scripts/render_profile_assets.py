"""Export GitHub profile graphics from the website-matched HTML source.

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
SCREENSHOT = ROOT / "scripts" / ".profile-assets-screenshot.png"
EDGE_PROFILE = ROOT / "scripts" / ".edge-render-profile"
EDGE = Path(r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe")
SCALE = 2
WINDOW = (1020, 743)

REGIONS = {
    "intro.png": (0, 0, 660, 250),
    "features.png": (0, 260, 1000, 405),
    "technologies.png": (0, 415, 1020, 533),
    "portfolio-button.png": (0, 543, 350, 633),
    "linkedin-button.png": (360, 543, 710, 633),
    "dribbble-button.png": (0, 643, 225, 733),
    "behance-button.png": (235, 643, 460, 733),
}


def safe_remove(path):
    resolved = path.resolve()
    if not resolved.is_relative_to(ROOT):
        raise RuntimeError(f"Refusing to remove a path outside the repository: {resolved}")
    if resolved.is_dir():
        shutil.rmtree(resolved)
    elif resolved.exists():
        resolved.unlink()


def main():
    if not EDGE.exists():
        raise RuntimeError(f"Microsoft Edge not found at {EDGE}")
    if SCREENSHOT.exists():
        safe_remove(SCREENSHOT)

    command = [
        str(EDGE),
        "--headless=new",
        "--disable-gpu",
        "--disable-extensions",
        "--hide-scrollbars",
        "--allow-file-access-from-files",
        "--run-all-compositor-stages-before-draw",
        "--virtual-time-budget=2500",
        f"--user-data-dir={EDGE_PROFILE}",
        f"--window-size={WINDOW[0]},{WINDOW[1]}",
        f"--force-device-scale-factor={SCALE}",
        f"--screenshot={SCREENSHOT}",
        SOURCE.as_uri(),
    ]
    subprocess.run(command, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, timeout=45)
    deadline = time.monotonic() + 20
    while not SCREENSHOT.exists() and time.monotonic() < deadline:
        time.sleep(0.2)
    if not SCREENSHOT.exists():
        raise RuntimeError("Edge did not create the screenshot")

    with Image.open(SCREENSHOT) as source:
        shot = source.convert("RGB")
    if shot.width < WINDOW[0] * SCALE or shot.height < WINDOW[1] * SCALE:
        raise RuntimeError(f"Unexpected screenshot size: {shot.size}")

    for name, region in REGIONS.items():
        box = tuple(value * SCALE for value in region)
        output = ROOT / "assets" / name
        shot.crop(box).save(output, optimize=True)
        print(f"{name}: {output.stat().st_size:,} bytes")

    safe_remove(SCREENSHOT)
    if EDGE_PROFILE.exists():
        try:
            safe_remove(EDGE_PROFILE)
        except PermissionError:
            print(f"Edge still uses temporary files in {EDGE_PROFILE}; remove them after it closes.")


if __name__ == "__main__":
    main()
