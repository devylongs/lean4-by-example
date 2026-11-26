-- Pattern matching
-- Give the first item of a list a different treatment from the empty case.

-- The empty list matches `[]`. A nonempty list matches `first :: rest`. The underscore discards the tail because the result only needs the head.
def firstOr (fallback : String) (names : List String) : String :=
  match names with
  | [] => fallback
  | first :: _ => first

-- Try the same function with each possible list shape.
#eval firstOr "Guest" ["Ada", "Lin"]
#eval firstOr "Guest" []
