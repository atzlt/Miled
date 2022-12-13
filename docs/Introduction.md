# The _Miled_ Language

_Miled_ is an esoteric language.

## Quick Tutorial

### The Very First Program

```
"Hello, world!"
```

This is a valid _Miled_ program, and it outputs `Hello, world`, as one would expect.

### Basic r=Rules

1. Put a space (or any whitespace symbol) between _any two_ lexemes.  This is because a word with no spaces will be
considered as an identifier, even starting with numbers. So for example, `+ 1 1` is correct, but `+1 1` is not.
**But** if a word starts with a quote `"`, it will be considered as the start of a string,
which ends at the next quote.

2. **Prefix notation**. The No. 1 rule to remember everywhere. So it's not `2 > 1`, it's `> 2 1`.

3. Functions automatically consumes input and executes. Imagine calling a function using the normal `f(x, y, ...)`
notation, but remove all commas and parentheses; that's how you call functions in _Miled_.

4. Since identifiers must be separated by whitespaces, _Miled_ accepts _any_ character in an identifier, unless a quote
appears as the first character. In this case _Miled_ would assume it's the beginning of a string.

### Function Calls

**Functions**, or more commonly appeared in the source code as **callers**, are basically automatically curried
functions. Take `+` as an example. `+` takes 2 parameters and return the sum of them. Remember that this language
uses _prefix notation_:

```
+ 1 2
```

outputs `3`. To show that it's curried we assign a partially-completed ("_unfulfilled_") caller to a variable:

```
:= x + 1 ;!
```

The `;!` at the end means "termination" (explained later), which basically stops `+` from consuming further inputs.
This time `x` has yet another parameter to fill in, so we call `x` directly:

```
:= x + 1 ;! x 2
```

outputs `3`.

There are 2 methods to force a caller to terminate and return. The first one, presented above, returns the unfulfilled
caller directly, and waits for further input. The second one, often called _enclosing_, fills the remaining input slots
with `None`, and executes it. If the arity of this caller is _indeterminate_, enclosing it will execute it immediately
with current arguments.

After a caller is executed, it doesn't wait for any more input, and will become an immediate value. For example

```
:= x + 1 ;! := y x 2 y
```

still outputs `3`. (Note: `:=` consumes only 2 parameters, so after `:= y x 2`, the `:=` caller is already fulfilled,
and the remaining `y` is returned.)

An example with indeterminate-arity callers:

```
:= x n+ ;! := x ;! x 1 ;! x 2 ;
```

`n+` is the indeterminate-arity version of `+`, which means it will consume all inputs until it's enclosed by `;` (at
the end of this program). Also notice the first `;!` in `:= x ;! x 1 ;!`, this is required, as if it's not present,
the interpreter will first try to evaluate the caller `x` first.

For a complete list of builtin callers, refer to [this document](./The Built-In Table.md).

***NOTICE THAT***, this language is somewhat **stack-based**, so once your parameter is pushed into the stack it cannot
be changed. Take this example:

```
:= x [ 1 2 3 ; push x pop x x
```

This code defines a list `x = [1, 2, 3]`, then push the popped value. But actually it returns `[1, 2, 3, 3]`! That's
because once `x = [1, 2, 3]` is in the stack of `push`, it is not changed since then. The right way is

```
:= x [ 1 2 3 ; pushto pop x x x
```

First pop, then push to stack. This returns `[1, 2, 3]`.

### Control Flow

```
if: ... :fi
if:: ... else ... :fi
while: ... :ihw
```

Nothing much to explain. Just be careful that `else` also closes all open branches (`if:`'s, `while:`'s) after the
nearest `if::`, and `:ihw` closes all open branches after the nearest `while:`. For example:

```
while: ... if: ... :ihw
```

is valid code.

### Caller Definition

```
def <name of caller> <list of param> <: ... :>
```

Still, nothing much to explain. Example:

```
def gcd /S "xy" <:
    if:: div min x y max x y min x y
    else gcd min x y % max x y min x y :fi
:>
def lgcd "x" <:
    while: >= len x 2 pushto gcd pop x pop x x :ihw
    @ x 0
:>
```
