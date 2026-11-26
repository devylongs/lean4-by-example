-- Do notation
-- Parse two inputs and add them only if both succeed.

-- Inside an `Option` computation, `←` extracts the value from `some`. Encountering `none` ends the computation immediately. The final `return` wraps the sum in `some`.
def addInputs (left right : String) : Option Nat := do
  let a ← left.toNat?
  let b ← right.toNat?
  return a + b

-- Changing the second input affects the whole result.
#eval addInputs "8" "5"
#eval addInputs "8" "five"
