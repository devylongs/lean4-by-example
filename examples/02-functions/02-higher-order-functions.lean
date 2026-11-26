-- Higher-order functions
-- Pass a transformation into another function.

-- Parentheses around `Nat → Nat` make the whole function type the type of one parameter.
def twice (step : Nat → Nat) (start : Nat) : Nat :=
  step (step start)

-- A `fun` expression constructs a function on the spot. Starting at three, double once to reach six and again to reach twelve.
#eval twice (fun n => n * 2) 3
