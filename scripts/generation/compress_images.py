#!/usr/bin/env python3
"""
File: compress_images.py
Path: scripts/generation/compress_images.py
Purpose: Compress tracked raster images to WebP and repoint every reference.

The preview-image generators (the `zer0-image-generator` gem and
scripts/lib/preview_generator.py) both emit PNG, which for AI-rendered artwork
runs ~2 MB a banner. Re-encoding those to WebP costs ~84% of the bytes at
visually indistinguishable quality, so this runs as a maintenance pass after a
generation run.

Idempotent: images already in WebP are left alone, and an image is only
replaced when the WebP is actually smaller. Animated GIFs are skipped (their
frame timing does not survive a naive re-encode).

Usage:
    python3 scripts/generation/compress_images.py --dry-run
    python3 scripts/generation/compress_images.py            # apply
    python3 scripts/generation/compress_images.py --quality 90
"""
from __future__ import annotations

import argparse
import io
import os
import subprocess
import sys

SOURCE_EXTS = (".png", ".jpg", ".jpeg", ".gif")
# Files whose contents may carry an image reference worth rewriting.
BINARY_EXTS = SOURCE_EXTS + (".webp", ".ico", ".woff", ".woff2", ".ttf", ".eot", ".pdf", ".zip")


def tracked_files() -> list[str]:
    out = subprocess.run(
        ["git", "ls-files"], capture_output=True, text=True, check=True
    ).stdout
    return [f for f in out.split("\n") if f]


def compress(path: str, quality: int) -> tuple[bytes, str] | None:
    """Return (webp_bytes, reason_if_skipped). None means 'convert it'."""
    from PIL import Image

    original_size = os.path.getsize(path)
    with Image.open(path) as im:
        if getattr(im, "n_frames", 1) > 1:
            return None, "animated"
        has_alpha = im.mode in ("RGBA", "LA") or (
            im.mode == "P" and "transparency" in im.info
        )
        frame = im.convert("RGBA" if has_alpha else "RGB")
        buf = io.BytesIO()
        frame.save(buf, "WEBP", quality=quality, method=6)

    if buf.tell() >= original_size:
        return None, "no gain"
    return buf.getvalue(), ""


def reference_forms(old: str, new: str) -> list[tuple[str, str]]:
    """Every textual spelling a reference to `old` can take.

    Front matter written by the preview generators honours `assets_prefix`, so
    `assets/images/x.png` on disk is spelled `/images/x.png` in a `preview:`
    key. Rewriting only the on-disk form silently leaves those pointing at a
    file that no longer exists.
    """
    forms = [(old, new)]
    prefix = "assets/"
    if old.startswith(prefix):
        forms.append((old[len(prefix):], new[len(prefix):]))
    return forms


def rewrite_references(mapping: dict[str, str], files: list[str]) -> int:
    """Point every textual reference at the new .webp path. Returns count."""
    expanded: dict[str, str] = {}
    for old, new in mapping.items():
        expanded.update(dict(reference_forms(old, new)))
    # Longest source paths first, so a shorter path never clobbers a longer one.
    pairs = sorted(expanded.items(), key=lambda kv: -len(kv[0]))
    total = 0
    for path in files:
        if path.lower().endswith(BINARY_EXTS):
            continue
        # `git ls-files` lists submodules as paths; they open as directories.
        if not os.path.isfile(path):
            continue
        try:
            original = open(path, encoding="utf-8").read()
        except (UnicodeDecodeError, FileNotFoundError, IsADirectoryError, OSError):
            continue
        updated = original
        for old, new in pairs:
            if old in updated:
                total += updated.count(old)
                updated = updated.replace(old, new)
        if updated != original:
            open(path, "w", encoding="utf-8").write(updated)
    return total


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--quality", type=int, default=82, help="WebP quality (default: 82)")
    parser.add_argument("--dry-run", action="store_true", help="Report only; change nothing")
    args = parser.parse_args()

    try:
        import PIL  # noqa: F401
    except ImportError:
        print("error: Pillow is required — pip install Pillow", file=sys.stderr)
        return 1

    files = tracked_files()
    images = [f for f in files if f.lower().endswith(SOURCE_EXTS)]

    mapping: dict[str, str] = {}
    before = after = 0
    skipped: list[tuple[str, str]] = []

    for path in images:
        size = os.path.getsize(path)
        before += size
        try:
            data, reason = compress(path, args.quality)
        except Exception as exc:  # a corrupt or unreadable image must not abort the pass
            skipped.append((path, f"error: {exc}"))
            after += size
            continue
        if data is None:
            skipped.append((path, reason))
            after += size
            continue

        dest = os.path.splitext(path)[0] + ".webp"
        after += len(data)
        mapping[path] = dest
        if not args.dry_run:
            with open(dest, "wb") as fh:
                fh.write(data)
            subprocess.run(["git", "rm", "-q", "--cached", path], check=False)
            os.remove(path)
            subprocess.run(["git", "add", dest], check=False)

    refs = 0 if args.dry_run else rewrite_references(mapping, files)

    verb = "would convert" if args.dry_run else "converted"
    print(f"{verb} {len(mapping)} images | skipped {len(skipped)}")
    if before:
        print(f"{before / 1048576:.1f} MB -> {after / 1048576:.1f} MB "
              f"({100 - 100 * after / before:.0f}% saved)")
    if not args.dry_run:
        print(f"rewrote {refs} references")
    for path, reason in skipped[:10]:
        print(f"  skip [{reason}] {path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
