-- Definitions and local names
-- Convert hours and minutes into a single duration.

-- A top-level definition is available throughout the rest of the file.
def minutesPerHour : Nat := 60

-- Parameters appear in parentheses. Inside the body, a `let` gives an intermediate result a local name. The last expression supplies the result.
def duration (hours minutes : Nat) : Nat :=
  let fromHours := hours * minutesPerHour
  fromHours + minutes

-- Apply a function by writing its arguments after its name, separated by spaces.
#eval duration 2 15
