-- Proof by induction
-- Show that copying a list preserves every element.

-- An empty list copies to an empty list. A nonempty list keeps its first element and recursively copies the tail.
def copyList {α : Type} : List α → List α
  | [] => []
  | x :: xs => x :: copyList xs

-- The proof follows the same structure as the function. In the nonempty case, `ih` says that copying the tail returns the tail. Simplification unfolds one step and uses that hypothesis.
theorem copyList_eq {α : Type} (xs : List α) : copyList xs = xs := by
  induction xs with
  | nil => rfl
  | cons x xs ih => simp only [copyList, ih]

#check copyList_eq
