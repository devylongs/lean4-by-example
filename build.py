"""Check the annotated Lean sources and render the static handbook."""
from concurrent.futures import ThreadPoolExecutor
from dataclasses import dataclass
from html import escape
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
    return Lesson(path.stem.split("-", 1)[1],
                  title, summary, blocks, source, result.stdout.rstrip("\n"), run_main)


def prose(value):
    return re.sub(r"`([^`]+)`", r"<code>\1</code>", escape(value))


TOKEN = re.compile(r'(?P<str>"(?:\\.|[^"\\])*")|(?P<num>\b[0-9]+\b)|'
                   r'(?P<kw>#eval|#check|\b(?:def|let|mut|if|then|else|fun|match|with|'
                   r'structure|where|deriving|inductive|class|instance|do|return|for|in|'
                   r'theorem|example|by|intro|exact|cases|induction|simp|only|rfl|rw|decide)\b)|'
                   r'(?P<ty>\b[A-Z]\w*)')


def highlight(source):
    parts = []
    start = 0
    for match in TOKEN.finditer(source):
        parts.extend((escape(source[start:match.start()]),
                      f'<span class="{match.lastgroup}">{escape(match[0])}</span>'))
        start = match.end()
    return "".join(parts) + escape(source[start:])


def layout(title, summary, page_class, body, base=""):
    return f"""<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>{escape(title)}</title><meta name="description" content="{escape(summary)}">
<link rel="stylesheet" href="{base}style.css"><script defer src="{base}site.js"></script></head>
<body><main class="{page_class}">{body}
<p class="footer">Based on <a href="https://gobyexample.com/">Go by Example</a> by Mark McGranaghan and Eli Bendersky |
<a href="https://github.com/mmcgrana/gobyexample">design source</a> |
<a href="https://creativecommons.org/licenses/by/3.0/">design license</a></p></main></body></html>"""


def lesson_page(lesson, following):
    filename = lesson.slug + ".lean"
    invocation = ("lean --run " if lesson.run_main else "lean ") + filename
    editor_source = lesson.source + ("\n#eval main\n" if lesson.run_main else "")
    editor = "https://live.lean-lang.org/#code=" + quote(editor_source, safe="")
    rows = "".join(f'<tr><td class="docs"><p>{prose(note)}</p></td>'
                   f'<td class="code"><pre><code class="snippet">{highlight(code)}</code></pre></td></tr>'
                   for note, code in lesson.blocks)
    next_link = (f'Next example: <a rel="next" href="../{following.slug}/index.html">{escape(following.title)}</a>.'
                 if following else '<a href="../index.html">Back to all examples</a>.')
    body = f"""<h1><a href="../index.html">{BOOK}</a>: {escape(lesson.title)}</h1>
<table><tbody><tr><td class="docs"><p>{escape(lesson.summary)}</p></td>
<td class="code empty"><div class="actions">
<button id="copy" hidden aria-label="Copy code" title="Copy code">⧉</button>
<a href="{editor}" aria-label="Run in Lean" title="Run in Lean">▶</a></div></td></tr>
{rows}<tr><td class="docs"><p>Save the <a download href="{filename}">source code</a>
as <code>{filename}</code> and run it with Lean.</p></td>
<td class="code terminal"><pre><span class="prompt">$</span> {invocation}
<samp>{escape(lesson.output)}</samp></pre></td></tr></tbody></table>
<p class="next">{next_link}</p>"""
    return layout(f"{BOOK}: {lesson.title}", lesson.summary, "example", body, "../")


def home(lessons):
    items = "\n".join(f'<li><a href="{item.slug}/index.html">{escape(item.title)}</a></li>'
                      for item in lessons)
    summary = "Learn functional programming and theorem proving with annotated Lean 4 examples."
    body = f"""<h1><a href="index.html">{BOOK}</a></h1>
<p><a href="https://lean-lang.org/">Lean</a> is a functional programming language and an interactive theorem prover.
The <a href="https://lean-lang.org/documentation/">official documentation</a> covers both.</p>
<p><em>{BOOK}</em> introduces programming and proving through annotated examples. Begin with the
<a href="{lessons[0].slug}/index.html">first example</a> or pick a topic from the list below.</p>
<p>The examples are checked with <a href="https://github.com/leanprover/lean4/releases/tag/v{VERSION}">Lean {VERSION}</a>.
Each example includes the code and the output from running it.</p>
<ul>{items}</ul>"""
    return layout(BOOK, summary, "intro", body)


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
        following = lessons[index + 1] if index + 1 < len(lessons) else None
        (folder / "index.html").write_text(lesson_page(lesson, following), encoding="utf-8")
        (folder / (lesson.slug + ".lean")).write_text(lesson.source, encoding="utf-8")
    for asset in ("style.css", "site.js"):
        shutil.copyfile(ROOT / "assets" / asset, DIST / asset)
    (DIST / "index.html").write_text(home(lessons), encoding="utf-8")
    print(f"Checked {len(lessons)} lessons with Lean {VERSION}. Open {DIST / 'index.html'}")


if __name__ == "__main__":
    main()
