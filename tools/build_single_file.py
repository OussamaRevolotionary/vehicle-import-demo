"""Build a self-contained copy of index.html with every asset inlined as a data URI.

Use the hosted page (index.html + assets/) for links. Use the single file when the
demo has to travel as an email attachment or be opened offline.

    python tools/build_single_file.py

Writes dist/Vehicle-Import-Platform-Demo.html.
"""
import base64
import mimetypes
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SRC = ROOT / "index.html"
OUT = ROOT / "dist" / "Vehicle-Import-Platform-Demo.html"

mimetypes.add_type("image/webp", ".webp")
mimetypes.add_type("video/webm", ".webm")

# Attributes whose value is an asset path to inline. <a href> to full-size shots
# is left alone on purpose: inlining those would double the file size.
ASSET_ATTR = re.compile(r'(\b(?:src|poster|content)=")(assets/[^"]+)(")')


def data_uri(rel_path: str) -> str:
    path = ROOT / rel_path
    mime = mimetypes.guess_type(path.name)[0] or "application/octet-stream"
    return f"data:{mime};base64,{base64.b64encode(path.read_bytes()).decode('ascii')}"


def main() -> None:
    html = SRC.read_text(encoding="utf-8")
    # Open Graph images must stay URLs; drop them from the offline build.
    html = re.sub(r'\s*<meta property="og:image[^>]*>', "", html)
    html = ASSET_ATTR.sub(lambda m: m.group(1) + data_uri(m.group(2)) + m.group(3), html)
    # Full-size links point at files that do not exist offline; unwrap them.
    html = re.sub(r'<a href="assets/[^"]+"[^>]*>(<img [^>]+>)</a>', r"\1", html)
    OUT.parent.mkdir(exist_ok=True)
    OUT.write_text(html, encoding="utf-8")
    print(f"Wrote {OUT.relative_to(ROOT)} ({OUT.stat().st_size / 1024:.0f} KB)")


if __name__ == "__main__":
    main()
