import time
import colorsys
import curses
import sys

from mote import Mote

from helper import clamp
from level import LevelState, FieldTile
from level_random import LevelRandom
from levels import START, LEVELS, Level1


# get the curses screen window
screen = curses.initscr()
# turn off input echoing
curses.noecho()
# respond to keys immediately (don't wait for enter)
curses.cbreak()
# map arrow keys to special values
screen.keypad(True)
screen.clear()

HUE_PLAYER = 0.333
HUE_TARGET = 0.667
HUE_OBSTAC = 0.0

ROWS = 4
COLS = 16

class Puzzled:
	def __init__(self, mote):
		self.mote = mote
		self.luma = 0.1
		self.field = [[FieldTile.EMPTY for x in range(COLS)] for y in range(ROWS)]
		self.cur_level_index = 0
		self.next_level()
		self.update_luma(0)

	def next_level(self):
		start = None
		if self.cur_level_index == 0:
			start = START
		else:
			start = self.current_level.target

		if self.cur_level_index < len(LEVELS):
			self.current_level = LEVELS[self.cur_level_index](self.field, start)
		else:
			self.current_level = LevelRandom(self.field, start)

	def start(self):
		self.running = True
		self.draw()
		self.loop()

	def stop(self):
		self.running = False

	def loop(self):
		while self.running:
			movement = self.get_input()
			moved = self.current_level.update(movement)

			if moved:
				if self.current_level.get_state() == LevelState.WON:
					self.cur_level_index += 1
					self.next_level()

				self.draw()

			screen.addstr(6, 0, str(movement[0]))
			screen.addstr(6, 2, str(movement[1]))
			time.sleep(0.05)

	def get_input(self):
		key = screen.getch()
		movement = [0, 0]
		if key == ord('q'):
			self.stop()
		elif key == ord('w'):
			self.update_luma(0.03)
		elif key == ord('e'):
			self.update_luma(-0.03)
		elif key == curses.KEY_UP:
			movement[0] -= 1
		elif key == curses.KEY_DOWN:
			movement[0] += 1
		elif key == curses.KEY_RIGHT:
			movement[1] += 1
		elif key == curses.KEY_LEFT:
			movement[1] -= 1

		return movement

	def update_luma(self, amount):
		def to_RGB(hue):
			tmp = colorsys.hsv_to_rgb(hue, 1, luma)
			return tuple(int(255 * x) for x in tmp)

		luma = clamp(self.luma + amount, 0.01, 1.0)
		self.COLOR_PLAYER = to_RGB(HUE_PLAYER)
		self.COLOR_TARGET = to_RGB(HUE_TARGET)
		self.COLOR_OBSTAC = to_RGB(HUE_OBSTAC)
		self.luma = luma
		self.draw()

	def draw(self):
		screen.clear()
		target = self.current_level.target
		for row in range(ROWS):
			channel = row + 1
			for col in range(COLS):
				color = [0, 0, 0]
				sign = ' '
				tile = self.field[row][col]
				if (tile == FieldTile.PLAYER):
					color = self.COLOR_PLAYER
					sign = '.'
				elif (tile == FieldTile.TARGET):
					color = self.COLOR_TARGET
					sign = 'O'
				elif (tile == FieldTile.OBSTAC):
					color = self.COLOR_OBSTAC
					sign = 'X'

				if self.mote != None:
					self.mote.set_pixel(channel, col, color[0], color[1], color[2])
				screen.addstr(row, col, sign)

		if self.mote != None:
			self.mote.show()
		screen.refresh()


def main():

	try:
		mote = None
		try:
			mote = Mote()
			mote.configure_channel(1, 16, False)
			mote.configure_channel(2, 16, False)
			mote.configure_channel(3, 16, False)
			mote.configure_channel(4, 16, False)
			mote.clear()
		except:
			pass

		puzzled = Puzzled(mote)
		puzzled.start()

		if mote != None:
			for channel in range(1, 5):
				for pixel in range(16):
					mote.set_pixel(channel, pixel, 0, 0, 0)
			mote.show()
		
		curses.nocbreak()
		screen.keypad(False)
		curses.echo()
		curses.endwin()
		quit()
	except:
		curses.nocbreak()
		screen.keypad(False)
		curses.echo()
		curses.endwin()
		print(sys.exc_info())

main()