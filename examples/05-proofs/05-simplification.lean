-- Simplification
-- Reduce an expression using facts Lean already knows.

-- The simplifier rewrites with a collection of lemmas marked for simplification. Here they remove addition by zero and multiplication by one.
theorem cleanTotal (n : Nat) : (0 + n) * 1 = n := by
  simp

-- To make the chosen rewrites explicit, list them after `simp only`.
example (n : Nat) : (0 + n) * 1 = n := by
  simp only [Nat.zero_add, Nat.mul_one]

#check cleanTotal
