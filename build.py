"""Check the annotated Lean sources and render the static handbook."""
from concurrent.futures import ThreadPoolExecutor
from dataclasses import dataclass
from html import escape
from itertools import groupby
from pathlib import Path
import re
import shutil
import subprocess
from tempfile import TemporaryDirectory
from urllib.parse import quote

ROOT = Path(__file__).resolve().parent
DIST = ROOT / "dist"
BOOK = "Lean 4 by Example"
VERSION = (ROOT / "lean-toolchain").read_text().strip().split(":v")[-1]


@dataclass
class Lesson:
    slug: str
    topic: str
    title: str
    summary: str
    blocks: list[tuple[str, str]]
    source: str
    output: str
    run_main: bool


def checked_lesson(path):
    header, body = path.read_text(encoding="utf-8").split("\n\n", 1)
    title, summary = (line.removeprefix("-- ") for line in header.splitlines())
    blocks = []
    for section in re.split(r"\n\n(?=-- )", body.strip()):
        lines = section.splitlines()
        if not lines[0].startswith("-- ") or len(lines) < 2:
            raise SystemExit(f"{path}: each block needs an annotation and Lean code.")
        note = lines.pop(0).removeprefix("-- ")
        blocks.append((note, "\n".join(lines).strip("\n")))
    source = "\n\n".join(code for _, code in blocks) + "\n"
    run_main = bool(re.search(r"^def main\b", source, re.M))
    cmd = ["lean", "-DwarningAsError=true"]
    if run_main:
        cmd.append("--run")
    # Run the exact source supplied by the download and copy controls.
    with TemporaryDirectory() as directory:
        snippet = Path(directory) / path.name
        snippet.write_text(source, encoding="utf-8")
        result = subprocess.run(cmd + [snippet], cwd=ROOT, text=True, capture_output=True)
    if result.returncode:
        raise SystemExit(f"{path}\n{result.stdout}{result.stderr}")
    topic = path.parent.name.split("-", 1)[-1].replace("-", " ").capitalize()
    return Lesson(path.stem.split("-", 1)[1], topic,
                  title, summary, blocks, source, result.stdout.rstrip("\n"), run_main)


def prose(value):
    return re.sub(r"`([^`]+)`", r"<code>\1</code>", escape(value))


TOKEN = re.compile(r'(?P<string>"(?:\\.|[^"\\])*")|(?P<number>\b[0-9]+\b)|'
                   r'(?P<keyword>#eval|#check|\b(?:def|let|mut|if|then|else|fun|match|with|'
                   r'structure|where|deriving|inductive|class|instance|do|return|for|in|'
                   r'theorem|example|by|intro|exact|cases|induction|simp|only|rfl|rw|decide)\b)|'
                   r'(?P<type>\b[A-Z]\w*)')


def highlight(source):
    parts = []
    start = 0
    for match in TOKEN.finditer(source):
        parts.extend((escape(source[start:match.start()]),
                      f'<span class="{match.lastgroup}">{escape(match[0])}</span>'))
        start = match.end()
    return "".join(parts) + escape(source[start:])


def page(title, description, content, base=""):
    return f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{escape(title)}</title>
<meta name="description" content="{escape(description)}">
<link rel="stylesheet" href="{base}style.css">
<script src="{base}site.js" defer></script>
</head>
<body><main>{content}</main>
<footer>by <a rel="author" href="https://github.com/devylongs">Longs Pemun Gotar</a>
 | <a href="https://github.com/devylongs/lean4byexample">source</a>
 | <a rel="license" href="https://creativecommons.org/licenses/by/3.0/">license</a></footer>
</body></html>"""


def lesson_page(lesson, previous, following):
    filename = lesson.slug + ".lean"
    command = ("lean --run " if lesson.run_main else "lean ") + filename
    editor_source = lesson.source + ("\n#eval main\n" if lesson.run_main else "")
    editor = "https://live.lean-lang.org/#code=" + quote(editor_source, safe="")
    examples = "".join(
        f'<figure><figcaption>{prose(note)}</figcaption>'
        f'<pre><code class="snippet">{highlight(code)}</code></pre></figure>'
        for note, code in lesson.blocks
    )
    back = (f'<a rel="prev" href="../{previous.slug}/index.html">← {escape(previous.title)}</a>'
            if previous else "")
    onward = (f'<a rel="next" href="../{following.slug}/index.html">{escape(following.title)} →</a>'
              if following else '<a href="../index.html">Return to contents</a>')
    content = f"""<nav class="breadcrumb" aria-label="Breadcrumb">
<a href="../index.html">{BOOK}</a> <span aria-hidden="true">/</span> {escape(lesson.topic)}</nav>
<article><header><h1>{escape(lesson.title)}</h1><p>{escape(lesson.summary)}</p></header>
<div class="tools"><a class="primary" href="{editor}">Open in Lean</a>
<button id="copy" type="button" hidden>Copy code</button>
<a download href="{filename}">Download .lean</a></div>
{examples}
<pre class="terminal" aria-label="Terminal"><code>$ {escape(command)}</code>
<samp>{escape(lesson.output)}</samp></pre></article>
<nav class="adjacent" aria-label="Adjacent lessons">{back}{onward}</nav>"""
    return page(f"{lesson.title} · {BOOK}", lesson.summary, content, "../")


def home(lessons):
    sections = []
    for topic, items in groupby(lessons, key=lambda lesson: lesson.topic):
        links = "".join(f'<li><a href="{item.slug}/index.html">{escape(item.title)}</a></li>'
                        for item in items)
        sections.append(f'<section><h2>{escape(topic)}</h2><ul>{links}</ul></section>')
    description = "Learn to write programs and check proofs in Lean 4, one working example at a time."
    first = lessons[0]
    content = f"""<header><h1>{BOOK}</h1><p>{description}</p>
<a class="primary" href="{first.slug}/index.html">Start with {escape(first.title)} →</a></header>
<nav class="contents" aria-label="Lesson index">{''.join(sections)}</nav>"""
    return page(BOOK, description, content)


def main():
    actual = subprocess.check_output(["lean", "--short-version"], cwd=ROOT, text=True).strip()
    if actual != VERSION:
        raise SystemExit(f"Expected Lean {VERSION}, found {actual}. Check lean-toolchain.")
    with ThreadPoolExecutor(max_workers=4) as pool:
        lessons = list(pool.map(checked_lesson, sorted((ROOT / "examples").glob("*/*.lean"))))
    if not lessons or len({item.slug for item in lessons}) != len(lessons):
        raise SystemExit("Expected lessons with unique slugs.")
    DIST.mkdir(exist_ok=True)
    for index, lesson in enumerate(lessons):
        folder = DIST / lesson.slug
        folder.mkdir(exist_ok=True)
        previous = lessons[index - 1] if index else None
        following = lessons[index + 1] if index + 1 < len(lessons) else None
        (folder / "index.html").write_text(lesson_page(lesson, previous, following), encoding="utf-8")
        (folder / (lesson.slug + ".lean")).write_text(lesson.source, encoding="utf-8")
    for asset in ("style.css", "site.js"):
        shutil.copyfile(ROOT / "assets" / asset, DIST / asset)
    (DIST / "index.html").write_text(home(lessons), encoding="utf-8")
    for obsolete in ("play.png", "clipboard.png"):
        (DIST / obsolete).unlink(missing_ok=True)
    print(f"Checked {len(lessons)} lessons with Lean {VERSION}. Open {DIST / 'index.html'}")


if __name__ == "__main__":
    main()
