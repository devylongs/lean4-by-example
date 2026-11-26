-- Conditions
-- Choose a shipping fee based on the order total.

-- An `if` expression produces a value. Both branches here produce a natural number.
def shippingFee (total : Nat) : Nat :=
  if total ≥ 50 then 0 else 5

-- Check both sides of the cutoff, including the total that qualifies for free shipping.
#eval shippingFee 49
#eval shippingFee 50
