-- Proof by cases
-- Prove that flipping a Boolean twice restores its value.

-- Define the operation by listing both Boolean inputs.
def flipSwitch : Bool → Bool
  | true => false
  | false => true

-- Splitting on `b` gives one goal for each constructor. In each case Lean can evaluate the two flips, and `rfl` finishes the proof.
theorem flipTwice (b : Bool) : flipSwitch (flipSwitch b) = b := by
  cases b with
  | false => rfl
  | true => rfl

#check flipTwice
