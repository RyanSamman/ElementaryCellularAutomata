import pygame
import thorpy
from random import randrange
from tkinter import messagebox, Tk
from tkinter import simpledialog
from CellularAutomata import CellularAutomata

class DisplayCellularAutomata:
	def __init__(self, width, height, rule, cellSize, initialState=None):
		pygame.init()
		pygame.font.init()

		# For the messagebox, to prevent a Tkinter window from popping up
		self.root = Tk()
		self.root.withdraw()

		self.MENU_HEIGHT = 75
		self.CELL_SIZE = cellSize
		self.CELLS_HEIGHT = height
		self.CELLS_WIDTH = width
		self.rule = rule
		self.CellularAutomata = CellularAutomata(width=self.CELLS_WIDTH, rule=rule)
		self.WINDOW_WIDTH = self.CELLS_WIDTH * self.CELL_SIZE
		self.WINDOW_HEIGHT = self.MENU_HEIGHT + self.CELLS_HEIGHT * self.CELL_SIZE
		self.window = pygame.display.set_mode((self.WINDOW_WIDTH, self.WINDOW_HEIGHT))
		self.Font = pygame.font.SysFont('Calibri', size=35)
		self.clock = pygame.time.Clock()

		self.COLOR = {
			'WHITE': (255, 255, 255),
			'BLACK': (000, 000, 000)
		}

		pygame.display.set_caption('Elementary Cellular Automata')

		self.setupUI()

		if initialState is None: self.resetCells()

		self.redraw()

		self.running = True
		while self.running:
			self.clock.tick(100)
			self.handleEvents()

	def handleEvents(self):
		for event in pygame.event.get():
			if event.type == pygame.QUIT: self.running = False
			if event.type == pygame.MOUSEBUTTONDOWN: self.handleClick(pygame.mouse.get_pos())
			self.menu.react(event)

	def handleClick(self, mousePos):
		x, y = mousePos
		if y >= self.MENU_HEIGHT:
			move = ((y - self.MENU_HEIGHT) // self.CELL_SIZE, x // self.CELL_SIZE)
			self.cells[move[1]] = int(not self.cells[move[1]])
			self.runCells()

	def runCells(self):
		self.CellularAutomata = CellularAutomata(width=self.CELLS_WIDTH, rule=self.rule, initialState=self.cells)
		for _ in range(self.CELLS_HEIGHT):
			self.CellularAutomata.applyRule()  # Generate next row
		self.redraw()  # Redraw window to display the next row

	def redraw(self):
		self.box.blit()
		self.box.update()
		self.displayRule()
		self.drawCells()
		pygame.display.update()

	def cellPos(self, y, x):
		return x * self.CELL_SIZE, self.MENU_HEIGHT + y * self.CELL_SIZE

	def drawCells(self):
		cells = [self.cells] + self.CellularAutomata.cellsHistory[1:]
		for y in range(len(cells)):
			for x in range(self.CELLS_WIDTH):
				if cells[y][x] != 1: continue
				pygame.draw.rect(
					self.window, 
					self.COLOR['BLACK'], 
					(x * self.CELL_SIZE, y * self.CELL_SIZE + self.MENU_HEIGHT, self.CELL_SIZE, self.CELL_SIZE)
				)
	
	def setupUI(self):
		BUTTON_SIZE = (120, 30) # Default Button Size, 120px wide and 30px high

		# Cell Buttons
		randomizeCellsButton = thorpy.make_button('Randomize Cells', func=self.randomizeCells)
		randomizeCellsButton.set_size(BUTTON_SIZE)

		resetCellsButton = thorpy.make_button('Reset Cells', func=self.resetCells)
		resetCellsButton.set_size(BUTTON_SIZE)
		
		cellButtons = [randomizeCellsButton, resetCellsButton]

		# Rule Buttons
		randomizeRuleButton = thorpy.make_button('Randomize Rule', func=self.randomizeRule)
		randomizeRuleButton.set_size(BUTTON_SIZE)

		setRulebutton = thorpy.make_button("Set Rule", func=self.setRule)
		setRulebutton.set_size(BUTTON_SIZE)

		ruleButtons = [randomizeRuleButton, setRulebutton]

		self.box = thorpy.Background(color=self.COLOR['WHITE'], elements= cellButtons + ruleButtons)
		thorpy.store(self.box, elements=cellButtons, align="left", x=0, y=0)
		thorpy.store(self.box, elements=ruleButtons, align="right", x=self.WINDOW_WIDTH, y=0)
		self.menu = thorpy.Menu(self.box)

		for element in self.menu.get_population():
			element.surface = self.window

		self.box.blit()
		self.box.update()

	def resetCells(self):
		sides = (self.CELLS_WIDTH - 1) // 2
		middle = self.CELLS_WIDTH - 2 * sides
		self.cells = [0] * sides + [1] * middle + [0] * sides
		self.runCells()
	
	def randomizeCells(self):
		self.cells = [randrange(0, 2) for _ in range(self.CELLS_WIDTH)]
		self.runCells()

	def randomizeRule(self):
		self.rule = randrange(0, 256) # Random rule from 0 to 255 (8 bit value/unsigned char / uint8)
		self.runCells()
	
	def setRule(self):
		answer = simpledialog.askinteger("Enter a rule", "Enter a rule from 0 to 255", parent=self.root, minvalue=0, maxvalue=255)
		if answer is None: return
		self.rule = answer
		self.runCells()

	def displayRule(self):
		ruleText = self.Font.render(f"Rule {self.rule}", True, self.COLOR['BLACK'])
		rect = ruleText.get_rect(center=(self.WINDOW_WIDTH // 2, self.MENU_HEIGHT // 2))
		self.window.blit(ruleText, rect)


def start_CellularAutomata():
	SCALE = 1; # You can play with this to get smaller cells for the same screen width, from 1 to 20 (Although it gets much slower)

	defaults = {
			'width': 61 * SCALE,
			'height': 40 * SCALE,
			'rule': 126,
			'cellSize': 20 // SCALE,
	}

	try:
		DisplayCellularAutomata(**defaults)
	except Exception as e:
		messagebox.showerror('ERROR', f'{e.__class__.__name__}: {e}')
		raise e


if __name__ == '__main__':
	start_CellularAutomata()