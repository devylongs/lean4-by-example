-- Reporting errors
-- Explain why a quantity was rejected.

-- An `Except String Nat` carries either a message or a natural number. Match first on the parse result, then on the shape of the number.
def quantity (input : String) : Except String Nat :=
  match input.toNat? with
  | none => .error "Enter a number"
  | some 0 => .error "Choose at least one"
  | some n => .ok n

-- Callers can distinguish malformed input from an order of zero items.
#eval quantity "x"
#eval quantity "0"
#eval quantity "3"
