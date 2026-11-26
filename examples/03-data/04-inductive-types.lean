-- Inductive types
-- Model three possible traffic signals.

-- Each constructor is one way to build a signal. Deriving `Repr` gives the interactive evaluator a way to print it.
inductive Signal where
  | stop
  | ready
  | go
  deriving Repr

-- A function defined by cases must cover every constructor. The leading dot lets Lean infer the constructor's type from context.
def nextSignal : Signal → Signal
  | .stop => .ready
  | .ready => .go
  | .go => .stop

-- Apply the transition twice, starting at the stop signal.
#eval nextSignal (nextSignal .stop)
