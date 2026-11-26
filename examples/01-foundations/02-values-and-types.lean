-- Values and types
-- Ask Lean for the value of an expression and the type of its result.

-- Use `#eval` for a calculation. Multiplication binds more tightly than addition.
#eval 2 + 3 * 4

-- Use `#check` to inspect a type. Lean infers `Nat` for a plain numeral and `Bool` for a Boolean literal.
#check 14
#check true

-- A type annotation changes how subtraction works. Natural numbers stop at zero, while integers can be negative.
#eval (2 : Nat) - 5
#eval (2 : Int) - 5
