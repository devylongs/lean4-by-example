# Lean 4 by Example

A hands-on introduction to programming and proving in Lean. Each lesson pairs short explanations with runnable code and shows the output captured from Lean.

## Read the handbook

Open `dist/index.html` in a browser after building. Start with Hello World or choose a topic from the index. Every lesson includes a source download and a link that loads its code in the Lean web editor.

## Build and check

Install Python 3.9 or later and Lean through [elan](https://lean-lang.org/install/). From this directory, run:

```sh
python3 build.py
```

The build uses the version in `lean-toolchain`, runs every example, treats Lean warnings as errors, and writes the static site to `dist/`. Python uses only its standard library. To serve the generated files over HTTP locally:

```sh
python3 -m http.server 8000 --bind 127.0.0.1 --directory dist
```

Visit `http://127.0.0.1:8000/`. The generated directory can also be served from a subdirectory on a static host.

## Add a lesson

Place a numbered `.lean` file in the appropriate group under `examples/`. Number prefixes set the reading order. The rest of the filename becomes the URL slug and must be unique. For example, `01-foundations/04-conditions.lean` produces `conditions/index.html`.

The first two comment lines give the title and summary. After a blank line, begin each code block with one comment explaining the code. Use backticks in the explanation for inline Lean expressions. The executable source is assembled from the code in order.

```lean
-- Squaring a number
-- Multiply a natural number by itself.

-- Both occurrences of `n` refer to the same input.
def square (n : Nat) : Nat := n * n

-- Evaluate the function at five.
#eval square 5
```

Use `#eval` to show a value and `#check` to inspect a type or theorem. A file defining `main` runs with `lean --run`. Rebuild to refresh the index, navigation, and captured output.
# lean4byexample
