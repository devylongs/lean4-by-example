-- Subtypes
-- Require a positive number at the boundary of a function.

-- The subtype packages a natural number with a proof of the predicate. Access the underlying number with `.val`.
def previous (n : { k : Nat // 0 < k }) : Nat :=
  n.val - 1

-- The caller provides both pieces. Lean checks the proof before evaluating the call.
#eval previous ⟨5, by decide⟩

-- Subtype values also expose their stored proof through `.property`.
example (n : { k : Nat // 0 < k }) : 0 < n.val :=
  n.property
