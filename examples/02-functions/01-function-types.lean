-- Function types
-- Supply one argument now and another later.

-- Read `Nat → Nat → Nat` from the right. Given one number, this function returns a function waiting for the next number.
def scaleBy (factor value : Nat) : Nat := factor * value
#check scaleBy

-- Supplying just the factor creates a new function. Lean infers the remaining argument and result types.
def triple := scaleBy 3
#check triple
#eval triple 8
