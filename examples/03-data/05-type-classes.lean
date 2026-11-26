-- Type classes
-- Give different kinds of values a shared way to produce a label.

-- A class describes an operation that depends on a type.
class Labeled (α : Type) where
  label : α → String

-- An instance supplies that operation for a particular type. Here a Boolean becomes a switch label.
instance : Labeled Bool where
  label enabled := if enabled then "on" else "off"

-- Square brackets request an instance. At this call Lean infers the type from `true` and finds the Boolean instance.
def displayLabel {α : Type} [Labeled α] (value : α) : String :=
  "[" ++ Labeled.label value ++ "]"

#eval displayLabel true
