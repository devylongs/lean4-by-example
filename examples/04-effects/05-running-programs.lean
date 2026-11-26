-- Running a program
-- Give a Lean file an entry point and run it from a terminal.

-- With `lean --run`, Lean looks for a definition named `main`. This one returns an I/O action whose result carries no further information.
def main : IO Unit := do
  IO.println "Starting the count"
  for n in [1, 2, 3] do
    IO.println n
