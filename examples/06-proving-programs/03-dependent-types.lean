-- Bounded indices
-- Choose an array position whose type carries a proof that it exists.

-- A value of `Fin n` is a natural number together with evidence that it is less than `n`. The index type here depends on the size of the particular array.
def pick {α : Type} (items : Array α) (i : Fin items.size) : α :=
  items[i]

-- Build the index from a position and its proof. The bound is concrete, so the tactic `decide` can check it by computation.
#eval pick #["north", "east", "south"] ⟨1, by decide⟩
