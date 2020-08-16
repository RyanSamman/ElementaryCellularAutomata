# Elementary Cellular Automata

A Real-Time implementation of [Wolfram Elementary Cellular Automata](https://mathworld.wolfram.com/ElementaryCellularAutomaton.html)


![Cellular Automata Display](./Images/CellularAutomataShowcase.gif)

# Explaination
You have a row of cells, and a cell's state in the next generation is influenced by the state of the surrounding cells and itself.

This leads us to have 8 possible states:

![Rules](https://mathworld.wolfram.com/images/eps-gif/ElementaryCA30Rules_750.gif)d 

Due to there being 8 states, each either `0` and `1`, there are `2**8`, or `256` possible Elementary Cellular Automata.

We can simplify these configurataions into "Rules", and this configuration, `0, 0, 0, 1, 1, 1, 1, 0` is the binary representation of the integer `30`

```
>>> int("00011110", 2)
```

Therefore, for a given value between `0` and `255`, we can generate an array which we can apply to the current generation

```
ruleArray = [rule >> i & 1 for i in range(8)]  # Converts bytes into array indexes (With Least Significant Bytes First)
```

And for each cell in the current generation, we can get the next generation's cells

```
index = 0
if left == 1:   index ^= 1  # 0b000 -> 0b001  Checks if the first byte is a 1
if middle == 1: index ^= 2  # 0b000 -> 0b010  Checks if the second byte is a 1
if right == 1:  index ^= 4  # 0b000 -> 0b100  Checks if the third byte is a 1
return ruleArray[index]
```

These simple rules lead to complex and interesting behavior, with some rules creating pseudo-random numbers, while others tend to reach a repeating pattern or die out completely.

In this project, the generations are placed from oldest (0th generation) to the nth generation, and you can quickly change the starting configuration and current rule to see the resulting cells.
