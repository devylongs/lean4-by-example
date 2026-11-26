-- Lists and folds
-- Transform a collection of prices and calculate their total.

-- A list contains values of one type. Mapping applies a function to each element in order.
def prices : List Nat := [3, 7, 2]
#eval prices.map (fun price => price * 2)

-- A left fold carries an accumulator from one element to the next. Here it starts at zero and grows by each price.
#eval prices.foldl (fun total price => total + price) 0
