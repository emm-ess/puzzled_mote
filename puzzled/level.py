from enum import Enum

class LevelState(Enum):
	RUNNING = 1
	WON = 2
	LOST = 3

class FieldTile(Enum):
	EMPTY = 1
	PLAYER = 2
	TARGET = 3
	OBSTAC = 4

class Level:
	def __init__(self, field, start):
		self.field = field
		self.start = start
		self.empty_field()
		self.reset_level()
		self.state = LevelState.RUNNING

	def reset_level(self):
		self.init_level()
		self.pos = [self.start[0], self.start[1]]
		self.set_tile(self.target, FieldTile.TARGET)
		self.set_tile(self.pos, FieldTile.PLAYER)

	def update(self, movement):
		self.restrict_movement(movement)
		moved = movement[0] != 0 or movement[1] != 0
		if moved:
			self.set_tile(self.pos, FieldTile.EMPTY)
			self.pos[0] += movement[0]
			self.pos[1] += movement[1]
			self.update_level(movement)
			self.evaluate_state()
			self.set_tile(self.pos, FieldTile.PLAYER)
		return moved

	def restrict_movement(self, movement):
		next_row = self.pos[0] + movement[0]
		next_col = self.pos[1] + movement[1]

		if (next_row < 0 or 3 < next_row):
			movement[0] = 0

		if (next_col < 0 or 15 < next_col):
			movement[1] = 0

	def evaluate_state(self):
		fieldTileAtPos = self.field[self.pos[0]][self.pos[1]]

		if self.state == LevelState.RUNNING:
			if fieldTileAtPos == FieldTile.OBSTAC:
				self.state = LevelState.LOST
				self.empty_field()
				self.set_tile(self.start, FieldTile.TARGET)
			elif fieldTileAtPos == FieldTile.TARGET:
				self.state = LevelState.WON
		elif self.state == LevelState.LOST and self.is_at_start():
			self.reset_level()
			self.state = LevelState.RUNNING

	def is_at_start(self):
		return self.pos[0] == self.start[0] and self.pos[1] == self.start[1]

	def set_tile(self, pos, tile_type):
		self.field[pos[0]][pos[1]] = tile_type

	def empty_field(self):
		for row in range(4):
			for col in range(16):
				self.field[row][col] = FieldTile.EMPTY

	def get_state(self):
		return self.state

	def init_level(self):
		pass

	def update_level(self, movement):
		pass