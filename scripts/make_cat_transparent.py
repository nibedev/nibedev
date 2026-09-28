"""Remove the charcoal matte from the existing animated cat GIF."""

from pathlib import Path

from PIL import Image, ImageChops, ImageSequence


ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "assets" / "cat-animated.gif"
TARGET = ROOT / "assets" / "cat-transparent.gif"
BACKGROUND = (13, 17, 23)


def main():
    with Image.open(SOURCE) as source:
        frames = []
        durations = []
        for frame in ImageSequence.Iterator(source):
            rgb = frame.convert("RGB")
            difference = ImageChops.difference(rgb, Image.new("RGB", rgb.size, BACKGROUND)).convert("L")
            alpha = difference.point(lambda value: 0 if value <= 3 else 255)
            rgba = rgb.convert("RGBA")
            rgba.putalpha(alpha)
            frames.append(rgba)
            durations.append(frame.info.get("duration", 40))
        frames[0].save(
            TARGET,
            save_all=True,
            append_images=frames[1:],
            duration=durations,
            loop=source.info.get("loop", 0),
            disposal=2,
            optimize=True,
        )
    with Image.open(TARGET) as result:
        result.seek(0)
        assert result.convert("RGBA").getpixel((0, 0))[3] == 0
        assert result.n_frames == len(frames)
        print(f"{TARGET.name}: {result.n_frames} frames, {TARGET.stat().st_size:,} bytes")


if __name__ == "__main__":
    main()
