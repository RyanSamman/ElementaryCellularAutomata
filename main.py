class CellularAutomata:
	def __init__(self, width=10, height=10, rule=0, initialState=None) -> None:
		if initialState is None:
			initialState = [0,0,0,0,1,1,0,0,0,0]
		self.WIDTH = width
		self.HEIGHT = height
		self.rule = rule
		self.cells = [initialState] + [[0] * width] * (height - 1)
		print(*self.cells, sep="\n")
		self.updateRuleArray()
		print(self.ruleArray)
	
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



if __name__ == "__main__":
	ca = CellularAutomata(rule=137)