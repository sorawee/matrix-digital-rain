#!/usr/bin/env python
#
# This file is adapted from Yu-Jie Lin's urtimer. Inspired by Tom Wallroth's
# matrix-curses.
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.

import random
import urwid
from urwid import raw_display

cols, rows = raw_display.Screen().get_cols_rows()

palette = [
    ('matrix', 'light green', 'black'),
    ('matrix-new', 'white', 'black')
]

class MatrixColumnWidget(urwid.Pile):
  signals = ['started']

  def __init__(self):
    self.mrows = [urwid.Text(' ') for x in range(rows)]
    self.__super.__init__(self.mrows)
    self.l = 0
    self.r = 0
    self.more = 0

  def update(self):
      if self.more == 0 and self.l == self.r:
          # let's not display immediately
          if random.randint(0, 5) != 0:
              return
          self.more = random.randint(rows // 3, rows - 1)
          self.l = random.randint(0, rows - 1)
          self.r = self.l
      if self.more != 0:
          # L[-1] == L[len - 1]!
          self.mrows[self.r - 1].set_text(('matrix', self.mrows[self.r - 1].get_text()[0]))
          self.mrows[self.r].set_text(('matrix-new' if self.more != 1 else 'matrix',
                                      random.choice("ɀɁɂŧϢϣϤϥϦϧϨϫϬϭϮϯϰϱϢϣϤϥϦϧϨϩϪϫϬϭϮϯϰ߃߄༣༤༥༦༧༩༪༫༬༭༮༯༰༱༲༳༶ ")))
          self.more -= 1
          self.r = (self.r + 1) % rows
      else:
          self.mrows[self.l].set_text(' ')
          self.l = (self.l + 1) % rows

def unhandled_input(key):
  if key in 'qQ':
    raise KeyboardInterrupt

def update_timer(loop, timer):
  timer.update()
  loop.set_alarm_in(0.1, update_timer, timer)
  
def start_update_timer(timer, loop):
  update_timer(loop, timer)

def main():
  global cols
  lst = [MatrixColumnWidget() for x in range(cols // 4)]
  loop = urwid.MainLoop(urwid.Filler(urwid.Columns(lst), valign='top'),
                        palette,
                        unhandled_input=unhandled_input)
  for col in lst:
      urwid.connect_signal(col, 'started', start_update_timer, loop)
      col._emit('started')
  try:
    loop.run()
  except KeyboardInterrupt:
    pass

if __name__ == '__main__':
  main()
