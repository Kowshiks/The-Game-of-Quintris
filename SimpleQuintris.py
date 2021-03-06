
from QuintrisGame import *

class SimpleQuintris(QuintrisGame):
  def __init__(self):
      QuintrisGame.__init__(self)

  def start_game(self, player):
    COMMANDS = { "b": self.left, "n": self.rotate, "m": self.right, "h": self.hflip }
    while 1:
      self.print_board(False)
      moves = player.get_moves(self)
      for c in moves:
        if c in COMMANDS:
          COMMANDS[c]()
        else:  
          raise "bad command!"
      self.down()          




