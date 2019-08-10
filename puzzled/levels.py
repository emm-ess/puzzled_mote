from level import Level, LevelState, FieldTile

class Level1(Level):
	def init_level(self):
		self.target = [0, 0]

class Level2(Level):
	def init_level(self):
		self.target = [0, 15]

class Level3(Level):
	def init_level(self):
		self.target = [2, 0]

		for col in range(3, 5):
			self.field[0][col] = FieldTile.OBSTAC
			self.field[1][col] = FieldTile.OBSTAC

		for col in range(8, 10):
			self.field[2][col] = FieldTile.OBSTAC
			self.field[3][col] = FieldTile.OBSTAC

class Level4(Level):
	def init_level(self):
		self.target = [1, 15]

		for col in range(3, 15):
			self.field[0][col] = FieldTile.OBSTAC
			self.field[3][col] = FieldTile.OBSTAC

		for col in range(6, 9):
			self.field[1][col] = FieldTile.OBSTAC

		for col in range(11, 15):
			self.field[2][col] = FieldTile.OBSTAC

class Level5(Level):
	def init_level(self):
		self.target = [1, 0]

		self.field[1][12] = FieldTile.OBSTAC
		self.field[2][12] = FieldTile.OBSTAC
		self.field[3][12] = FieldTile.OBSTAC

		self.field[0][9] = FieldTile.OBSTAC
		self.field[1][9] = FieldTile.OBSTAC
		self.field[3][9] = FieldTile.OBSTAC

		self.field[0][6] = FieldTile.OBSTAC
		self.field[2][6] = FieldTile.OBSTAC
		self.field[3][6] = FieldTile.OBSTAC

		self.field[0][3] = FieldTile.OBSTAC
		self.field[1][3] = FieldTile.OBSTAC
		self.field[2][3] = FieldTile.OBSTAC

class Level6(Level):
	def init_level(self):
		self.target = [2, 15]
		self.movement_count = 0

	def update_level(self, movement):
		self.movement_count += 1

		if self.movement_count > 4:
			col = self.movement_count - 4
			for row in range(4):
				self.field[row][col] = FieldTile.OBSTAC

class Level7(Level):
	def init_level(self):
		self.target = [0, 7]
		self.movement_count = 0

	def update_level(self, movement):
		self.movement_count += 1

		if self.movement_count > 3:
			col = 15 - self.movement_count + 3
			for row in range(4):
				self.field[row][col] = FieldTile.OBSTAC

		if self.movement_count > 4:
			col = self.movement_count - 4
			for row in range(4):
				self.field[row][col] = FieldTile.OBSTAC



START = [3, 0]
LEVELS = [Level1, Level2, Level3, Level4, Level5, Level6, Level7]