-- Hello World
-- Print a greeting and see where Lean displays the result.

-- A string is text enclosed in double quotes. Give this one a name with `def` and declare its type as `String`.
def greeting : String := "Hello, world!"

-- `IO.println` builds an action that prints one line. The `#eval` command runs it. In a Lean editor, place the cursor on this line to see the message.
#eval IO.println greeting
