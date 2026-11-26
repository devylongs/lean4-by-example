-- Loops and local mutation
-- Count the words that meet a minimum length.

-- An `Id.run` block allows imperative syntax inside a pure function. The `mut` binding can be reassigned on each pass through the loop.
def countLong (words : List String) (minimum : Nat) : Nat := Id.run do
  let mut count := 0
  for word in words do
    if word.length ≥ minimum then
      count := count + 1
  return count

-- Only the last two words reach four characters.
#eval countLong ["elm", "cedar", "pine"] 4
