-- Optional values
-- Use a missing result to represent a failed lookup.

-- String parsing returns an `Option Nat`. A valid input produces a number wrapped in `some`. Other inputs produce `none`.
#eval "24".toNat?
#eval "two".toNat?

-- Map a transformation over the possible number. Lean applies it only when the parser found a value.
def nextNumber (text : String) : Option Nat :=
  text.toNat?.map (fun n => n + 1)

#eval nextNumber "24"
#eval nextNumber "two"
