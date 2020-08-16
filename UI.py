import pygame
import thorpy
from random import randrange
from tkinter import messagebox, Tk
from tkinter import simpledialog
from CellularAutomata import CellularAutomata

class DisplayCellularAutomata:
	def __init__(self, width, height, rule, initialState=None):
		pygame.init()
		pygame.font.init()

		self.MENU_HEIGHT = 65
		self.CELL_SIZE = 20
		self.CELLS_HEIGHT = height
		self.CELLS_WIDTH = width
		self.rule = rule
		self.CellularAutomata = CellularAutomata(width=self.CELLS_WIDTH, rule=rule)
		self.WINDOW_WIDTH = self.CELLS_WIDTH * self.CELL_SIZE
		self.WINDOW_HEIGHT = self.MENU_HEIGHT + self.CELLS_HEIGHT * self.CELL_SIZE
		self.window = pygame.display.set_mode((self.WINDOW_WIDTH, self.WINDOW_HEIGHT))
		self.Font = pygame.font.SysFont('Calibri', 35)
		self.clock = pygame.time.Clock()

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
		self.window.fill((255, 255, 255))
		self.box.blit()
		self.box.update()
		pygame.draw.rect(self.window, (255, 255, 255), (50, 75, 300, 300))
		self.drawCells()
		self.displayRule()
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
					(0, 0, 0), 
					(x * self.CELL_SIZE, y * self.CELL_SIZE + self.MENU_HEIGHT, self.CELL_SIZE, self.CELL_SIZE)
				)
	
	def setupUI(self):
		# runButton = thorpy.make_button('  Run  ', func=lambda: self.runCells())
		# runButton.set_main_color((145, 195, 220))

		randomizeCellsButton = thorpy.make_button('Randomize Cells', func=lambda: self.randomizeCells())
		resetCellsButton = thorpy.make_button("    Reset Cells    ", func=lambda: self.resetCells())
		cell_Es = [randomizeCellsButton, resetCellsButton]

		randomizeRuleButton = thorpy.make_button('Randomize Rule', func=lambda: self.randomizeRule())
		setRulebutton = thorpy.make_button("     Set Rule     ", func=lambda: self.setRule(50))

		rule_Es = [randomizeRuleButton, setRulebutton]

		self.box = thorpy.Background(color=(255, 255, 255),elements= cell_Es + rule_Es)
		thorpy.store(self.box, elements=cell_Es, align="left", x=0, y=0)
		thorpy.store(self.box, elements=rule_Es, align="left", x=120, y=0)
		# thorpy.store(self.box, elements=[runButton], y=0, x=(self.WINDOW_WIDTH - 30))
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
		self.rule = randrange(0, 256)
		self.runCells()
	
	def setRule(self, newRule):
		answer = simpledialog.askinteger("Enter a rule", "Enter a rule from 0 to 255", parent=root, minvalue=0, maxvalue=255)
		if answer is None: return
		self.rule = answer
		self.runCells()

	def displayRule(self):
		ruleText = self.Font.render(f"Rule {self.rule}", True, (0, 0, 0))
		rect = ruleText.get_rect(center=(self.WINDOW_WIDTH // 2, 20))
		self.window.blit(ruleText, rect)


def start_CellularAutomata():
	# For the messagebox, to prevent a Tkinter window from popping up
	root = Tk()
	root.withdraw()
	
	try:
		DisplayCellularAutomata(width=51, height=40, rule=126)
	except Exception as e:
		messagebox.showerror('ERROR', f'{e.__class__.__name__}: {e}')
		raise e


if __name__ == '__main__':
	start_CellularAutomata()