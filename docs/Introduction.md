# The _Miled_ Language: An Introduction

_Miled_ is an esoteric language. The goal of this language is to become as weird as possible.

I want to make a language that

1. Uses **prefix notation**,
2. **Curries** all functions, and

Keeping these basic rules in mind might be helpful to understand some grammar rules.

## Quick Tutorial

### The Very First Program

```
"Hello, world!"
```

This is a valid _Miled_ program, and it outputs `Hello, world`, as one would expect.

### Basic rules

1. Put a space (or any whitespace symbol) between _any two_ lexemes.  This is because a word with no spaces will be
considered as an identifier, even starting with numbers. So for example, `+ 1 1` is correct, but `+1 1` is not.
**But** if a word starts with a quote `"`, it will be considered as the start of a string,
which ends at the next quote.

2. **Prefix notation**. The No. 1 rule to remember everywhere. So it's not `2 > 1`, it's `> 2 1`.

3. Functions antomatically consumes input and executes. Imagine calling a function using the normal `f(x, y, ...)`
4. notation, but remove all commas and parentheses; that's how you call functions in _Miled_.

### Function calls

**Functions**, or more commonly appeared in the source code as **callers**, are basically automatically curried
functions. Take `+` as an example. `+` takes 2 parameters and return the sum of them. Remember that this language
uses _prefix notation_:

```
+ 1 2
```

outputs `3`. To show that it's curried we assign a partially-completed ("_unfulfilled_") caller to a variable:

```
let x + 1 ;!
```

The `;!` at the end means "termination" (explained later), which basically stops `+` from consuming further inputs.
This time `x` has yet another parameter to fill in, so we call `x` directly:

```
let x + 1 ;! x 2
```

outputs `3`.

There are 2 methods to force a caller to terminate and return. The first one, presented above, returns the unfulfilled
caller directly, and waits for further input. The second one, often called _enclosing_, fills the remaining input slots
with `None`, and executes it. If the arity of this caller is _indeterminate_, enclosing it will execute it immediately
with current arguments.

After a caller is executed, it doesn't wait for any more input, and will become an immediate value. For example

```
let x + 1 ;! let y x 2 y
```

still outputs `3`. (Note: `let` consumes only 2 parameters, so after `let y x 2`, the `let` caller is already fulfilled,
and the remaining `y` is returned.)

An example with indeterminate-arity callers:

```
let x n+ ;! let x ;! x 1 ;! x 2 ;
```

`n+` is the indeterminate-arity version of `+`, which means it will consume all inputs until it's enclosed by `;` (at
the end of this program). Also notice the first `;!` in `let x ;! x 1 ;!`, this is required, as if it's not present,
the interpreter will first try to evaluate the caller `x` and then assign value to the result.

### Control Flow (WIP)
