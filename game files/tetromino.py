from tile import Tile  
from point import Point  
import copy as cp  
import random 
import numpy as np  
import lib.stddraw as stddraw
from lib.color import Color 
class Tetromino:
   grid_height, grid_width = None, None
   def __init__(self, shape):
      self.type = shape  
      occupied_cells = []
      if self.type == 'I':
         n = 4  
         occupied_cells.append((1, 0))  
         occupied_cells.append((1, 1))
         occupied_cells.append((1, 2))
         occupied_cells.append((1, 3))
      elif self.type == 'O':
         n = 2  
         occupied_cells.append((0, 0))  
         occupied_cells.append((1, 0))
         occupied_cells.append((0, 1))
         occupied_cells.append((1, 1))
      elif self.type == 'Z':
         n = 3  
         occupied_cells.append((0, 1))  
         occupied_cells.append((1, 1))
         occupied_cells.append((1, 2))
         occupied_cells.append((2, 2))
      elif self.type == 'T':
         n = 3
         occupied_cells.append((0, 1))
         occupied_cells.append((1, 1))
         occupied_cells.append((2, 1))
         occupied_cells.append((1, 2))
      elif self.type == 'S':
         n = 3
         occupied_cells.append((1, 1))
         occupied_cells.append((2, 1))
         occupied_cells.append((0, 2))
         occupied_cells.append((1, 2))
      elif self.type == 'J':
         n = 3
         occupied_cells.append((0, 0))
         occupied_cells.append((0, 1))
         occupied_cells.append((1, 1))
         occupied_cells.append((2, 1))
      elif self.type == 'L':
         n = 3
         occupied_cells.append((2, 0))
         occupied_cells.append((0, 1))
         occupied_cells.append((1, 1))
         occupied_cells.append((2, 1))
   
      self.tile_matrix = np.full((n, n), None)
      for i in range(len(occupied_cells)):
         col_index, row_index = occupied_cells[i][0], occupied_cells[i][1]
         self.tile_matrix[row_index][col_index] = Tile()
         
      for row in range(n):
         for col in range(n):
            if self.tile_matrix[row][col] is not None:
               number = 2 if random.random() < 0.7 else 4
               self.tile_matrix[row][col].number = number

      self.bottom_left_cell = Point()
      self.bottom_left_cell.y = Tetromino.grid_height - 1
      self.bottom_left_cell.x = random.randint(0, Tetromino.grid_width - n)

   def get_cell_position(self, row, col):
      n = len(self.tile_matrix)  
      position = Point()
      position.x = self.bottom_left_cell.x + col
      position.y = self.bottom_left_cell.y + (n - 1) - row
      return position

   def get_min_bounded_tile_matrix(self, return_position=False):
      n = len(self.tile_matrix)  
      min_row, max_row, min_col, max_col = n - 1, 0, n - 1, 0
      for row in range(n):
         for col in range(n):
            if self.tile_matrix[row][col] is not None:
               if row < min_row:
                  min_row = row
               if row > max_row:
                  max_row = row
               if col < min_col:
                  min_col = col
               if col > max_col:
                  max_col = col
      copy = np.full((max_row - min_row + 1, max_col - min_col + 1), None)
      for row in range(min_row, max_row + 1):
         for col in range(min_col, max_col + 1):
            if self.tile_matrix[row][col] is not None:
               row_ind = row - min_row
               col_ind = col - min_col
               copy[row_ind][col_ind] = cp.deepcopy(self.tile_matrix[row][col])
      if not return_position:
         return copy
      else:
         blc_position = cp.copy(self.bottom_left_cell)
         blc_position.translate(min_col, (n - 1) - max_row)
         return copy, blc_position

   def draw(self):
      n = len(self.tile_matrix)  
      for row in range(n):
         for col in range(n):
            if self.tile_matrix[row][col] is not None:
               position = self.get_cell_position(row, col)
               if position.y < Tetromino.grid_height:
                  self.tile_matrix[row][col].draw(position)

   def move(self, direction, game_grid):
      if not (self.can_be_moved(direction, game_grid)):
         return False  
      if direction == "left":
         self.bottom_left_cell.x -= 1
      elif direction == "right":
         self.bottom_left_cell.x += 1
      else:  
         self.bottom_left_cell.y -= 1
      return True  

   def can_be_moved(self, direction, game_grid):
      n = len(self.tile_matrix)  
      if direction == "left" or direction == "right":
         for row_index in range(n):
            for col_index in range(n):
               row, col = row_index, col_index
               if direction == "left" and self.tile_matrix[row][col] is not None:
                  leftmost = self.get_cell_position(row, col)
                  if leftmost.x == 0:
                     return False  
                  if game_grid.is_occupied(leftmost.y, leftmost.x - 1):
                     return False  
                  break  
               row, col = row_index, n - 1 - col_index
               if direction == "right" and self.tile_matrix[row][col] is not None:
                  rightmost = self.get_cell_position(row, col)
                  if rightmost.x == Tetromino.grid_width - 1:
                     return False  
                  if game_grid.is_occupied(rightmost.y, rightmost.x + 1):
                     return False  
                  break  
      else:
         for col in range(n):
            for row in range(n - 1, -1, -1):
               if self.tile_matrix[row][col] is not None:
                  bottommost = self.get_cell_position(row, col)
                  if bottommost.y == 0:
                     return False  
                  
                  if game_grid.is_occupied(bottommost.y - 1, bottommost.x):
                     return False  
                  break  
      return True  

   def rotate_clockwise(self, game_grid):
   
      
      n = len(self.tile_matrix)
      rotated_matrix = np.full((n, n), None)
      
      for row in range(n):
         for col in range(n):
            if self.tile_matrix[row][col] is not None:
               rotated_matrix[col][n-1-row] = self.tile_matrix[row][col]
      
      if not self.can_be_rotated(rotated_matrix, game_grid):
         return False  
      
      self.tile_matrix = rotated_matrix
      return True

   def rotate_counter_clockwise(self, game_grid):
      
      
      n = len(self.tile_matrix)
      rotated_matrix = np.full((n, n), None)
      
      for row in range(n):
         for col in range(n):
            if self.tile_matrix[row][col] is not None:
               rotated_matrix[n-1-col][row] = self.tile_matrix[row][col]
      
      if not self.can_be_rotated(rotated_matrix, game_grid):
         return False  
      
      self.tile_matrix = rotated_matrix
      return True
   
   def can_be_rotated(self, rotated_matrix, game_grid):
      n = len(rotated_matrix)
      
      for row in range(n):
         for col in range(n):
            if rotated_matrix[row][col] is not None:
               position = self.get_cell_position(row, col)
               
               if (position.x < 0 or position.x >= Tetromino.grid_width or
                   position.y < 0 or position.y >= Tetromino.grid_height):
                  return False
               
               if game_grid.is_occupied(position.y, position.x):
                  current_pos = False
                  for curr_row in range(n):
                     for curr_col in range(n):
                        if self.tile_matrix[curr_row][curr_col] is not None:
                           curr_position = self.get_cell_position(curr_row, curr_col)
                           if curr_position.x == position.x and curr_position.y == position.y:
                              current_pos = True
                              break
                     if current_pos:
                        break
                  
                  if not current_pos:
                     return False
      
      return True
