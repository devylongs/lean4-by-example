-- Verifying a function
-- Implement a list transformation, then prove a property for every input.

-- Replace each element of a list with zero. A sample run shows what happens on one input.
def zeros : List Nat → List Nat
  | [] => []
  | _ :: xs => 0 :: zeros xs

#eval zeros [8, 2, 5]

-- State the property for any list. In the inductive step, both lengths grow by one. The induction hypothesis identifies the lengths of the tails.
theorem zeros_length (xs : List Nat) : (zeros xs).length = xs.length := by
  induction xs with
  | nil => rfl
  | cons x xs ih => simp only [zeros, List.length_cons, ih]

#check zeros_length
