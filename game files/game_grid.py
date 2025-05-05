import copy
from tile import Tile
from point import Point
import lib.stddraw as stddraw
from lib.color import Color
import numpy as np


class GameGrid:
   def check_connections(self):
    for row in range(self.grid_height):
        for col in range(self.grid_width):
            if self.tile_matrix[row][col] is not None:
                self.tile_matrix[row][col].is_connected = False

    for col in range(self.grid_width):
        if self.tile_matrix[0][col] is not None:
            self.tile_matrix[0][col].is_connected = True

    for _ in range(10):  
        self.up_sweep()
        self.left_sweep()
        self.right_sweep()

   def up_sweep(self):
    for row in range(1, self.grid_height):
        for col in range(self.grid_width):
            if self.tile_matrix[row][col] is not None:
                if self.tile_matrix[row - 1][col] is not None and self.tile_matrix[row - 1][col].is_connected:
                    self.tile_matrix[row][col].is_connected = True

   def left_sweep(self):
    for row in range(1, self.grid_height):
        for col in range(1, self.grid_width):
            if self.tile_matrix[row][col] is not None:
                if self.tile_matrix[row][col - 1] is not None and self.tile_matrix[row][col - 1].is_connected:
                    self.tile_matrix[row][col].is_connected = True

   def right_sweep(self):
    for row in range(1, self.grid_height):
        for col in range(self.grid_width - 2, -1, -1):
            if self.tile_matrix[row][col] is not None:
                if self.tile_matrix[row][col + 1] is not None and self.tile_matrix[row][col + 1].is_connected:
                    self.tile_matrix[row][col].is_connected = True

   def drop_tile(self, row, col):
    while row > 0 and self.tile_matrix[row][col] is not None and self.tile_matrix[row - 1][col] is None:
        self.tile_matrix[row - 1][col] = self.tile_matrix[row][col]
        self.tile_matrix[row][col] = None
        row -= 1


   def eliminate_floating_pieces(self):
    self.check_connections()
    for row in range(self.grid_height):
        for col in range(self.grid_width):
            if self.tile_matrix[row][col] is not None:
                if not self.tile_matrix[row][col].is_connected:
                    self.drop_tile(row, col)
    self.check_connections()



   def __init__(self, grid_h, grid_w):
      self.grid_height = grid_h
      self.grid_width = grid_w
      self.tile_matrix = np.full((grid_h, grid_w), None)
      self.current_tetromino = None
      self.next_tetromino = None
      self.game_over = False
      self.score = 0

      self.empty_cell_color = Color(42, 69, 99)
      self.line_color = Color(0, 100, 200)
      self.boundary_color = Color(0, 100, 200)
      self.line_thickness = 0.002
      self.box_thickness = 10 * self.line_thickness

   def display(self):

    self.eliminate_floating_pieces()

    if self.current_tetromino is not None:
        self.current_tetromino.draw()           

       


    while True:
      merged = False
      is_merge_possible, row1, col1 = self.merge_possible()
      if is_merge_possible:
        self.merge_tiles(row1, col1)
        merged = True
        self.eliminate_floating_pieces()
      if not merged:
        break


    stddraw.clear(self.empty_cell_color)


    self.draw_grid()


    if self.current_tetromino is not None:
        self.current_tetromino.draw()


    self.draw_boundaries()


    stddraw.setFontSize(20)
    stddraw.setPenColor(Color(255, 255, 255))
    stddraw.text(self.grid_width + 1, self.grid_height - 1, "SCORE")

    stddraw.setFontSize(16)
    stddraw.text(self.grid_width + 1, self.grid_height - 2, f"{self.score}")
    

    stddraw.setFontSize(20)
    stddraw.setPenColor(Color(255, 255, 255))
    stddraw.text(self.grid_width + 1, self.grid_height - 4, "NEXT")
    

    if self.next_tetromino is not None:
        self.draw_next_tetromino()


    stddraw.show(250)


   def draw_next_tetromino(self):
      if self.next_tetromino is None:
         return
         

      tile_matrix = self.next_tetromino.tile_matrix
      n = len(tile_matrix)  
      

      center_x = self.grid_width + 1
      center_y = self.grid_height - 7  
      

      for row in range(n):
         for col in range(n):
            if tile_matrix[row][col] is not None:

               pos_x = center_x + (col - n/2 + 0.5)
               pos_y = center_y - (row - n/2 + 0.5)
               

               tile_matrix[row][col].draw(Point(pos_x, pos_y))


   def clear_full_rows(self):
    rows_cleared = 0
    for row in range(self.grid_height):
        full = True
        row_sum = 0
        for col in range(self.grid_width):
            tile = self.tile_matrix[row][col]
            if tile is None:
                full = False
                break
            else:
                row_sum += tile.number

        if full:

            self.score += row_sum
            rows_cleared += 1


            for col in range(self.grid_width):
                self.tile_matrix[row][col] = None

            for r in range(row, self.grid_height - 1):
                for c in range(self.grid_width):
                    self.tile_matrix[r][c] = self.tile_matrix[r + 1][c]


            for c in range(self.grid_width):
                self.tile_matrix[self.grid_height - 1][c] = None


            row -= 1
    return rows_cleared
   
   def merge_possible(self):
    for col in range(self.grid_width):
        for row in range(self.grid_height - 1):
            current = self.tile_matrix[row][col]
            above = self.tile_matrix[row + 1][col]
            if current is not None and above is not None:
                if current.number == above.number:
                    return True, row, col
    return False, -1, -1
   def merge_tiles(self, row, col):
    tile1 = self.tile_matrix[row][col]
    tile2 = self.tile_matrix[row + 1][col]
    
    if tile1 is not None and tile2 is not None and tile1.number == tile2.number:
        tile1.number *= 2
        self.tile_matrix[row + 1][col] = None
        self.score += tile1.number
        self.eliminate_floating_pieces()
   def drop_floating_tiles(self):
    for col in range(self.grid_width):
        for row in range(1, self.grid_height):
            if self.tile_matrix[row][col] is not None and self.tile_matrix[row - 1][col] is None:
                current_row = row
                while current_row > 0 and self.tile_matrix[current_row - 1][col] is None:
                    self.tile_matrix[current_row - 1][col] = self.tile_matrix[current_row][col]
                    self.tile_matrix[current_row][col] = None
                    current_row -= 1

   def draw_grid(self):
      for row in range(self.grid_height):
         for col in range(self.grid_width):
            if self.tile_matrix[row][col] is not None:
               self.tile_matrix[row][col].draw(Point(col, row))
      stddraw.setPenColor(self.line_color)
      stddraw.setPenRadius(self.line_thickness)
      start_x, end_x = -0.5, self.grid_width - 0.5
      start_y, end_y = -0.5, self.grid_height - 0.5
      for x in np.arange(start_x + 1, end_x, 1):  
         stddraw.line(x, start_y, x, end_y)
      for y in np.arange(start_y + 1, end_y, 1):  
         stddraw.line(start_x, y, end_x, y)
      stddraw.setPenRadius()  

   def draw_boundaries(self):
      stddraw.setPenColor(self.boundary_color)  
      stddraw.setPenRadius(self.box_thickness)
      pos_x, pos_y = -0.5, -0.5
      stddraw.rectangle(pos_x, pos_y, self.grid_width, self.grid_height)
      stddraw.setPenRadius()  

   def is_occupied(self, row, col):
      if not self.is_inside(row, col):
         return False  
      return self.tile_matrix[row][col] is not None

   def is_inside(self, row, col):
      if row < 0 or row >= self.grid_height:
         return False
      if col < 0 or col >= self.grid_width:
         return False
      return True

   def update_grid(self, tiles_to_lock, blc_position):
    self.current_tetromino = None
    n_rows, n_cols = len(tiles_to_lock), len(tiles_to_lock[0])
    for col in range(n_cols):
        for row in range(n_rows):
            if tiles_to_lock[row][col] is not None:
                pos = Point()
                pos.x = blc_position.x + col
                pos.y = blc_position.y + (n_rows - 1) - row
                if self.is_inside(pos.y, pos.x):
                    self.tile_matrix[pos.y][pos.x] = tiles_to_lock[row][col]
                else:
                    self.game_over = True

    while True:
        is_merge_possible, row1, col1 = self.merge_possible()
        if not is_merge_possible:
            break
        self.merge_tiles(row1, col1)  #

    self.clear_full_rows()

    self.eliminate_floating_pieces()

    if self.next_tetromino is not None:
        self.current_tetromino = self.next_tetromino
        self.next_tetromino = None
    return self.game_over

   def has_empty_cells(self):
    for row in range(self.grid_height):
        for col in range(self.grid_width):
            if self.tile_matrix[row][col] is None:
                return True
    return False
   def check_win_condition(self):
    for row in range(self.grid_height):
        for col in range(self.grid_width):
            if (self.tile_matrix[row][col] is not None and 
                self.tile_matrix[row][col].number >= 2048):
                return True
    return False



