-- Arrays and indexing
-- Append a name and look up an element by position.

-- Array literals begin with a hash. The result of `push` contains the extra entry.
def names := #["Ada", "Lin"]
def extended := names.push "Sam"
#eval names.size
#eval extended.size

-- Positions start at zero. Optional indexing returns `some` for an existing entry and `none` for a position outside the array.
#eval extended[2]?
#eval extended[3]?
