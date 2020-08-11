from random import randrange


class CellularAutomata:
    def __init__(self, width=11, rule=0, initialState=None) -> None:
        if initialState is None:  # Create an array with stuff in the center
            sides = (width - 1) // 2
            middle = width - 2 * sides
            initialState = [0] * sides + [1] * middle + [0] * sides

        self.WIDTH = width
        self.cellsHistory = [[*initialState]]
        self.cells = initialState[:]  # Copy the array
        self.rule = rule
        self.updateRuleArray()

    def updateRuleArray(self):
        """
            Little endian version (Least significant bytes first) (wikipedia is big endian)
            There are 8 possible variants
            Left empty (0), current empty (0), and Right empty (0)
            this can be shortened to 000


            000 001 010 011 100 101 110 111
            [1,  0,  1,  0,  0,  1,  0,  1];

            Ex. 137 -> 0b10001001
            checks if first bit ^ is 1
            >> then shifts the bytes left
            1000100
            is    ^ 1? if so, result is 1, else, 0
        """
        # Converts bytes to little endian array of bytes
        self.ruleArray = [self.rule >> i & 1 for i in range(8)]

    def generateRuleIndex(self, left, middle, right):
        index = 0
        if self.cells[left]:   index ^= 1  # 0b000 -> 0b001
        if self.cells[middle]: index ^= 2  # 0b000 -> 0b010
        if self.cells[right]:  index ^= 4  # 0b000 -> 0b100
        return self.ruleArray[index]

    def applyRule(self):
        newCells = []
        for i, _ in enumerate(self.cells):
            left = (i - 1) % self.WIDTH
            right = (i + 1) % self.WIDTH
            newCells.append(self.generateRuleIndex(left, i, right))
        self.cells = newCells
        self.cellsHistory.append(newCells)
        return newCells

    @staticmethod
    def displayCells(cells):
        [print("\033[1;40m__\033[1;m" if c else "__", end="") for c in cells]
        print()


if __name__ == "__main__":
    inputRule = randrange(0, 255)  # int(input("Enter a rule: "))
    print(f"Rule {inputRule}")
    width = 61
    startarr = [randrange(0, 2) for i in range(width)]
    print("Starting cells are", startarr)
    height = 40
    ca = CellularAutomata(rule=inputRule, width=width, initialState=startarr)
    ca.displayCells(ca.cells)
    for _ in range(height):
        ca.applyRule()
        ca.displayCells(ca.cells)
