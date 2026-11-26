-- Polymorphism
-- Write a function that works on a pair of any two types.

-- Braces mark implicit parameters. Lean infers `α` and `β` from the pair. The result type records the reversed order.
def exchange {α β : Type} (pair : α × β) : β × α :=
  (pair.2, pair.1)

-- The same definition works with different component types.
#eval exchange ("row", 4)
#eval exchange (true, "ready")
