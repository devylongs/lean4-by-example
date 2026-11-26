-- Implication
-- Turn two implications into a single proof from start to finish.

-- Read `P → Q` as a function taking evidence of `P` to evidence of `Q`. A `by` block lets us construct a proof with tactics.
theorem chain {P Q R : Prop} (first : P → Q) (second : Q → R) :
    P → R := by
  intro hp
  exact second (first hp)

-- After `intro hp`, the goal is `R` with a hypothesis `hp : P`. Applying the first implication gives evidence of `Q`, which the second turns into evidence of `R`.
#check chain
