-- Structural recursion
-- Compute the sum of the natural numbers up to a limit.

-- Zero has no predecessors to add. In the successor case, use the answer for the smaller argument `n`. Lean checks that recursion eventually reaches the base case.
def sumUpTo : Nat → Nat
  | 0 => 0
  | n + 1 => sumUpTo n + (n + 1)

-- At four the calculation adds one, two, three, and four.
#eval sumUpTo 0
#eval sumUpTo 4
