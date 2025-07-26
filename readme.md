# DPO

## Description

This is a backend which performs DPO evolution algorithm, it has only one endpoint at `POST /evolve/` it calculates a hypergraph and returns a json with it.

## Frontend?

Frontend is an editor made to work with custom dsl for the graph creation, it will have a special functions which would work only in max msp `web` module, and output dicts specific for music creation. The dsl would have some special context-aware features, made for pre-exec caching and variables' temporary storage

## Stack to use

### Frontend

- Typescript

- Svelte

- ANTLR4ts

- Monaco Editor

### Backend 

- Python

- FastAPI

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
3. This python code can suit as backend api, frontend should have a dsl editor, that would send requests to the api when needed to calculate a graph. both api and frontend should have redis cache base

## Name suggestions

### 1. Syntagma

### 2. Nomothetes

### 3. Diakrisis

## Frontend

So, there is a canvas/editor, which can return the position, or store some context of hooks and listeners

There is an instanse of the dsl compiler, that checks if you pressed enter (or just a new line of code appeared), it tries to read out the code and if it's correct execute it right away, the instance of anything that you registered in dsl, frontend stores along with it's declaration position in editor, when you erase the line, the instance deletes itself, but stays in cache (for a case if you just want to redeclare something or edit)

## Caching

let there be a function 

```ts
check_cache(func())
// if found -> redis cache 
// if not -> func()
```