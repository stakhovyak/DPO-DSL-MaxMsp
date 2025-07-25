# DPO

## DSL proto

```cpp
// creating modules (variables)
// seed ≔ (A) >>> exp.add_module("seed", {"<uuid>":["A"]})
// branch ≔ (x y)(x z) >>> exp.add_module("branch", {...})
seed = (A)
branch = (x, y)(x, z)
triple = (x, y, b)

// creating and registering rules
@grow = seed -> seed -> branch // if the variable has @prefix in name it means that it is treated as a rule and has to be initializated by L -> I -> R syntax

// what happens under the hood
// rb = RuleBuilder().from_modules(exp.modules["seed"],exp.modules["seed"],exp.modules["branch"])
// exp.set_rule("grow", rb.build())

// could be also written as
@grow1 = (x) -> (x) -> (x, y, b)(x, y)

$start = seed // exp.states["start"] = exp.modules["seed"]
$new_state = $start <~ @grow 5 // exp.apply("start", "grow", 5)
// basically we create a variable here = seed and then rewrite it applied @grow to it 5 times

// making variables is optional because you can do it like so

$new_state = (A) <~ (A) -> (A) -> (x,y)(y,z) 5 // same as $start <~ @grow 5 
```

## TODO I must come up with syntax and concept of outputting $states to the musical context

### Things to consider

1. The generation of the states could be a pretty time consuming process, so you can't use it for sounds immediately as it declarated, so this language is more like a compiled one
2. The moment the state comes into the composition should be synchronized with max msp global transport
3. So there must be a bin folder with scripts such as ./bin/load_script ./composition1.dsl