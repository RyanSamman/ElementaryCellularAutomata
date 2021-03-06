from random import randrange


class CellularAutomata:
    def __init__(self, width=11, rule=0, initialState=None) -> None:
        if initialState is None:  # Create an array with stuff in the center
            sides = (width - 1) // 2
            middle = width - 2 * sides
            initialState = [0] * sides + [1] * middle + [0] * sides

        self.CELLS_WIDTH = width
        self.cellsHistory = [[*initialState]]  # Record the history of the cells
        self.cells = initialState
        self.rule = rule
        self.updateRuleArray()

    def updateRuleArray(self):
        # Converts bytes to little endian array of bytes
        self.ruleArray = [self.rule >> i & 1 for i in range(8)]

    def generateRuleIndex(self, left, middle, right):
        index = 0b000
        if self.cells[left]:   index ^= 0b001  # 0b000 -> 0b001
        if self.cells[middle]: index ^= 0b010  # 0b000 -> 0b010
        if self.cells[right]:  index ^= 0b100  # 0b000 -> 0b100
        return self.ruleArray[index]

    def applyRule(self):
        newCells = []
        for currentPosition, _ in enumerate(self.cells):
            left = (currentPosition - 1) % self.CELLS_WIDTH
            right = (currentPosition + 1) % self.CELLS_WIDTH
            newCells.append(self.generateRuleIndex(left, currentPosition, right))

        self.cells = newCells
        self.cellsHistory.append(newCells)
        return newCells

    @staticmethod
    def displayCells(cells):
        [print("[]" if c else "__", end="") for c in cells]
        print()


if __name__ == "__main__":
    # Testing in the CLI, the main entrypoint is UI.py
    inputRule = randrange(0, 256)  # int(input("Enter a rule: "))
    print(f"Rule {inputRule}")
    width = 61
    height = 40
    startarr = [randrange(0, 2) for i in range(width)]
    print("Starting cells are", startarr)
    ca = CellularAutomata(rule=inputRule, width=width, initialState=startarr)
    ca.displayCells(ca.cells)
    for _ in range(height):
        ca.applyRule()
        ca.displayCells(ca.cells)
