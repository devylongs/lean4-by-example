-- Structures
-- Describe a location with named fields and move it east.

-- A structure combines fields into a single type. Deriving `Repr` lets Lean display values of that type during evaluation.
structure Point where
  x : Int
  y : Int
  deriving Repr

-- Record update syntax starts with an existing point. Only the listed field receives a new value.
def east (p : Point) : Point :=
  { p with x := p.x + 1 }

-- The argument type tells Lean which structure the field names belong to.
#eval east { x := 2, y := -1 }
