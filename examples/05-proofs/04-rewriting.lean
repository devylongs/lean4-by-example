-- Rewriting
-- Use a known equality to replace a term inside a larger expression.

-- The hypothesis `h` identifies the two inputs. The tactic `rw [h]` replaces `a` with `b` in the goal, then closes the resulting reflexive equality.
theorem sameTotal (a b fee : Nat) (h : a = b) :
    a + fee = b + fee := by
  rw [h]

-- The fee can be any natural number because the proof only uses equality of the inputs.
#check sameTotal
