-- Equality and reflexivity
-- Ask Lean to check a statement that follows by computation.

-- Doubling a number here means adding it to itself.
def twiceNat (n : Nat) : Nat := n + n

-- A theorem names a proposition and supplies its proof. Lean can reduce both sides to six, so reflexivity (`rfl`) proves this equality.
theorem doubleThree : twiceNat 3 = 6 := rfl

-- Inspect the theorem. Its type is the statement it proves.
#check doubleThree
