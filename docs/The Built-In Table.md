# The Built-In Table

Some callers are for control flows, and are thus not presented here.

## Essentials

| Caller |                 Usage                 | Function                                                                                                                    |
|:------:|:-------------------------------------:|:----------------------------------------------------------------------------------------------------------------------------|
|  `<-`  |            `<- var value`             | Assign value to variable. **Notice that** this also works for variables not in the current scope.                           |
|  `:=`  |            `:= var value`             | Assign value to variable. **Notice that** this works in the current scope; if the variable is not present then creates one. |
|  `~`   |          `~ stmt stmt ... ;`          | Continuation. Only returns the last output.                                                                                 |
|  `o>`  |               `o> val`                | Output the value.                                                                                                           |
| `def`  | `def id list-of-param-id <: stmts :>` | Define a caller.                                                                                                            |
|  `fn`  |   `fn list-of-param-id <: stmts :>`   | Define an inline anonymous caller.                                                                                          |

### Operators

|                  Caller                   |     Usage      | Function                  |
|:-----------------------------------------:|:--------------:|:--------------------------|
|      `+`, `-`, `*`, `/`, `//`, `**`       |  `+ val val`   | Same as Python operators. |
|    `+=`, `-=`, `*=`, `/=`, `//=` `**=`    | `+= var value` | Calculate then assign.    |
|                `n+`, `n*`                 |                | `n`-ary forms.            |
|                `0-`, `0-=`                |                | Unary minus.              |
|                `-!`, `-=!`                |                | Absolute difference.      |
|     `>`, `<`, `>=`, `<=`, `==`, `!=`      |                | Comparisons               |
| `&`, `&=`, `!`, `=!`, `&vert;`, `&vert;=` |                | Boolean operations.       |

### Type Conversions

They're the same as Python's builtin functions.

| Caller  | Function                   |
|:-------:|:---------------------------|
| `->str` | Convert to string          |
| `->int` | Convert to int             |
| `->ord` | Convert ASCII to int       |
| `->chr` | Convert to ASCII           |
| `->cpx` | Convert to complex         |
| `->dec` | Convert to decimal (float) |
| `->lst` | Convert to list            |

## More Things

### List and String Manipulation

|    Caller     |       Usage        | Function                                                                                                   |
|:-------------:|:------------------:|:-----------------------------------------------------------------------------------------------------------|
|     `rev`     |     `rev list`     | Reverse (same as Python `.reverse()`)                                                                      |
|    `sort`     |    `sort list`     | Sort (same as Python `.sort()`)                                                                            |
|     `lst`     |     `lst list`     | Last element (same as Python `[-1]`)                                                                       |
|     `fst`     |     `fst list`     | First element (same as Python `[0]`)                                                                       |
|     `len`     |     `len list`     | Length (same as Python `len()`)                                                                            |
|    `push`     |  `push list val`   | Push (same as Python `.append()`)                                                                          |
|   `pushto`    | `pushto val list`  | Push (same as Python `.append()`)                                                                          |
|     `pop`     |     `pop list`     | Pop and return (same as Python `.pop()`)                                                                   |
|     `..=`     |   `..= num num`    | Range, inclusive.                                                                                          |
|     `..<`     |   `..< num num`    | Range, exclude the ending index.                                                                           |
|     `:.<`     | `:.< num num num`  | Range, exclude the ending index, with step.                                                                |
|     `@?`      |   `@? list val`    | First index of `val` in `list`.                                                                            |
| `[:]`, `[::]` | `[:] list num num` | Same as Python slices.                                                                                     |
|      `@`      |    `@ list num`    | List access.                                                                                               |
|     `@<-`     | `@<- list num val` | Change the value at index.                                                                                 |
|     `+@`      | `+@ list num val`  | Append `val` before index `num` in `list`.                                                                 |
|     `-@`      |   `+@ list num`    | Pop and return the value at index.                                                                         |
|     `cS`      |      `cS str`      | Split (same as Python `.split("")`                                                                         |
|     `wS`      |      `wS str`      | Split by whitespace (same as Python `.split()`)                                                            |
|     `,S`      |      `,S str`      | Split by comma (same as Python `.split(",")`)                                                              |
|    `join`     |  `join str list`   | Join by string (same as Python `.join()`                                                                   |
|     `map`     |   `map fn list`    | Map `fn` over the list and return the new list.<br/>**Notice that** `fn` should at least take 1 parameter. |

### Mathematics

For callers with note `(n)`, adding `n` to it forms its `n`-ary form.
For callers with note `(l)`, adding `l` to it forms its list form.

|         Caller / Variable         |   Usage   | Function                                              |
|:---------------------------------:|:---------:|:------------------------------------------------------|
|       `(nl)max`, `(nl)min`        | `max x y` | Maximum and minimum (same as Python `max()`, `min()`) |
| `abs`, `sqrt`, `sin`, `cos`, `ln` |           | You know what these mean, right?                      |
|         `PI`, `EE`, `II`          |           | Same as Python `math.pi`, `math.e`, `1j`              |
|               `rnd`               |   `rnd`   | Random number in `[0, 1)`.                            |
|              `rnd#`               | `rnd# n`  | Random integer in `[0, n]`.                           |

#### Number-Theoretic

| Caller / Variable |       Usage       | Function                                                                                |
|:-----------------:|:-----------------:|:----------------------------------------------------------------------------------------|
|       `div`       | `div small large` | Divides. Returns `bool`.                                                                |
|     `(nl)gcd`     |                   | **G**reatest **c**ommon **d**ivisor.                                                    |
|      `prim?`      |                   | Is it **prim**e?                                                                        |
|      `prim@`      |                   | The `n`-th **prim**e.                                                                   |
|      `prim]`      |     `prim] n`     | A list of the first `n` primes.                                                         |
|      `pFctS`      |                   | **P**rime **f**a**ct**ors as a **s**et                                                  |
|      `pFctM`      |                   | **P**rime **f**a**ct**ors as a **m**ultiset                                             |
|      `pFctE`      |                   | **P**rime **f**a**ct**ors in **e**xponential form, e.g. `[(2, 3), (3, 8), (7, 1), ...]` |
|      `#pFct`      |                   | The number of distinct prime factors                                                    |
|     `#pFctM`      |                   | The number of primes, counting multiplicities                                           |
|  `divs`, `#divs`  |                   | Divisors, the number of divisors, resp.                                                 |
|     `eulPhi`      |                   | The Euler Phi function, a.k.a. totient function.                                        |
|      `coprm`      |                   | All the **copr**i**m**e numbers less than `n`.                                          |
