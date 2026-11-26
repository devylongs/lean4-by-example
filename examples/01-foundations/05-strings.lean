-- Strings and interpolation
-- Build a message from text and a number.

-- The `++` operator joins two strings.
#eval "Lean" ++ " 4"

-- Inside an interpolated string, braces enclose an expression. Lean converts the result into text.
def receipt (item : String) (price : Nat) : String :=
  s!"{item} costs {price} credits."

-- Printing a string displays its contents without quotation marks.
#eval IO.println (receipt "Tea" 3)
