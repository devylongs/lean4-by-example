-- Conjunction
-- Swap the two pieces of evidence in an “and” statement.

-- A proof of `P ∧ Q` contains both a proof of `P` and a proof of `Q`. Use projections to take them apart and angle brackets to put them together in the new order.
theorem swapAnd {P Q : Prop} (h : P ∧ Q) : Q ∧ P :=
  ⟨h.2, h.1⟩

-- The proposition parameters are implicit. Lean recovers them from the evidence when the theorem is applied.
#check swapAnd
