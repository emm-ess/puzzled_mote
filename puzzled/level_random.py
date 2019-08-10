import random
from level import Level, LevelState, FieldTile

class LevelRandom(Level):
	def init_level(self):
		self.target = [random.randint(0,3), random.randint(0,15)]

		for row in range(4):
			for col in range(16):
				if (random.random() < 0.1) and self.field[row][col] == FieldTile.EMPTY:
					self.field[row][col] = FieldTile.OBSTAC
