import sys
import threading
from playsound import playsound
import lib.stddraw as stddraw
from lib.picture import Picture
from lib.color import Color
import os
from game_grid import GameGrid
from tetromino import Tetromino
from tile import Tile
import random



def play_background_music():
    try:
        music_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), "sounds", "main_music.wav")
        print(f"Müzik dosyası yolu: {music_path}")
        
        if os.path.exists(music_path):
            while True: 
                playsound(music_path)  
                if not game_started or is_paused: 
                    break
        else:
            print(f"Müzik dosyası bulunamadı: {music_path}")
    except Exception as e:
        print(f"Müzik çalma hatası: {e}")


is_paused = False
game_started = False
need_restart = False
game_speed = 40

button_colors = {
    "MEDIUM": Color(25, 255, 228),
    "HARD": Color(25, 255, 228),
    "EXIT": Color(25, 255, 228)
}


def display_pause_menu(grid_height, grid_width):
    background_color = Color(42, 69, 99)
    button_color = Color(25, 255, 228)
    text_color = Color(31, 160, 239)
    overlay_color = Color(0, 0, 0)
    
    panel_w, panel_h = grid_width / 2, grid_height / 2
    panel_x = (grid_width + 4.5) / 2 - panel_w / 2
    panel_y = grid_height / 2 - panel_h / 2
    
    current_dir = os.path.dirname(os.path.realpath(__file__))
    background_img_file = os.path.join(current_dir, "images", "dirt_background.jpg")
    background_image = Picture(background_img_file)
    
    stddraw.setPenColor(overlay_color)
    stddraw.filledRectangle(-0.5, -0.5, grid_width + 5, grid_height)
    
    stddraw.picture(background_image, panel_x + panel_w / 2, panel_y + panel_h / 2)
    
    stddraw.setPenColor(Color(31, 160, 239))
    stddraw.setPenRadius(0.003)
    stddraw.rectangle(panel_x, panel_y, panel_w, panel_h)
    
    button_w = panel_w - 1
    button_h = 1.5
    button_spacing = 2
    
    current_dir = os.path.dirname(os.path.realpath(__file__))
    resume_button_file = os.path.join(current_dir, "menu_images", "resume_game_button.png")
    restart_button_file = os.path.join(current_dir, "menu_images", "restart_game_button.png")
    exit_button_file = os.path.join(current_dir, "menu_images", "exit_button.png")
    resume_button_image = Picture(resume_button_file)
    restart_button_image = Picture(restart_button_file)
    exit_button_image = Picture(exit_button_file)
    
    stddraw.setFontFamily("Arial")
    stddraw.setFontSize(20)
    stddraw.setPenColor(text_color)
    stddraw.boldText(panel_x + panel_w / 2, panel_y + panel_h - 0.5, "PAUSED")
    
    button_y = panel_y + panel_h - 3.5
    stddraw.picture(resume_button_image, panel_x + panel_w / 2, button_y + button_h / 2)
    
    button_y -= button_spacing
    stddraw.picture(restart_button_image, panel_x + panel_w / 2, button_y + button_h / 2)
    
    button_y -= button_spacing
    stddraw.picture(exit_button_image, panel_x + panel_w / 2, button_y + button_h / 2)
    
    return panel_x + 0.5, panel_y, button_w, panel_h


def start():
    global need_restart, is_paused, game_speed, game_started
    
    game_started = True  
    
    try:
        print("Müzik thread'i başlatılıyor...")
        music_thread = threading.Thread(target=play_background_music, daemon=True)
        music_thread.start()
        print("Müzik thread'i başlatıldı")
    except Exception as e:
        print(f"Müzik thread'i başlatma hatası: {e}")
    
    grid_h, grid_w = 20, 12
    
    canvas_h = 40 * grid_h
    canvas_w = 40 * (grid_w + 5)
    
    stddraw.setCanvasSize(canvas_w, canvas_h)
    stddraw.setXscale(-0.5, grid_w + 4.5)
    stddraw.setYscale(-0.5, grid_h - 0.5)
    
    Tetromino.grid_height = grid_h
    Tetromino.grid_width = grid_w
    grid = GameGrid(grid_h, grid_w)
    
    current_tetromino = create_tetromino()
    next_tetromino = create_tetromino()
    
    grid.current_tetromino = current_tetromino
    grid.next_tetromino = next_tetromino
    
    display_game_menu(grid_h, grid_w)
    
    while True:
        if need_restart:
            need_restart = False
            is_paused = False
            grid = GameGrid(grid_h, grid_w)
            current_tetromino = create_tetromino()
            next_tetromino = create_tetromino()
            grid.current_tetromino = current_tetromino
            grid.next_tetromino = next_tetromino
        
        if stddraw.hasNextKeyTyped():
            key_typed = stddraw.nextKeyTyped()
            if key_typed == "escape":
                is_paused = True
                grid.display()
                panel_x, panel_y, button_w, panel_h = display_pause_menu(grid_h, grid_w)
                stddraw.show(50)
                
                while is_paused:
                    if stddraw.mousePressed():
                        mouse_x, mouse_y = stddraw.mouseX(), stddraw.mouseY()
                        
                        if (panel_x <= mouse_x <= panel_x + button_w and 
                            panel_y + panel_h - 3.5 <= mouse_y <= panel_y + panel_h - 2):
                            is_paused = False
                            break
                        
                        elif (panel_x <= mouse_x <= panel_x + button_w and 
                              panel_y + panel_h - 5.5 <= mouse_y <= panel_y + panel_h - 4):
                            need_restart = True
                            is_paused = False
                            break
                        
                        elif (panel_x <= mouse_x <= panel_x + button_w and 
                              panel_y + panel_h - 7.5 <= mouse_y <= panel_y + panel_h - 6):
                            sys.exit()
                    
                    stddraw.show(50)
            
            if key_typed == "left":
                current_tetromino.move(key_typed, grid)
            elif key_typed == "right":
                current_tetromino.move(key_typed, grid)
            elif key_typed == "down":
                current_tetromino.move(key_typed, grid)
            elif key_typed == "up":
                current_tetromino.rotate_clockwise(grid)
            elif key_typed == "z":
                current_tetromino.rotate_counter_clockwise(grid)
            
            stddraw.clearKeysTyped()
        
        if not is_paused:
            success = current_tetromino.move("down", grid)
            grid.eliminate_floating_pieces()

            if not success:
                tiles, pos = current_tetromino.get_min_bounded_tile_matrix(True)
                game_over = grid.update_grid(tiles, pos)
                
                if not grid.has_empty_cells():
                    display_lose_screen(grid_h, grid_w)
                    break
                
                if grid.check_win_condition():
                    display_win_screen(grid_h, grid_w)
                    break
                
                if game_over:
                    break
                
                next_tetromino = create_tetromino()
                grid.next_tetromino = next_tetromino
                current_tetromino = grid.current_tetromino
            
            grid.display()
            stddraw.show(game_speed)
    
    print("Game over")


def create_tetromino():
    tetromino_types = ['I', 'O', 'Z', 'T', 'S', 'J', 'L']
    random_index = random.randint(0, len(tetromino_types) - 1)
    random_type = tetromino_types[random_index]
    tetromino = Tetromino(random_type)
    return tetromino


def display_game_menu(grid_height, grid_width):
    current_dir = os.path.dirname(os.path.realpath(__file__))
    background_img_file = os.path.join(current_dir, "images", "dirt_background.jpg")
    background_image = Picture(background_img_file)
    
    stddraw.picture(background_image, (grid_width + 4.5) / 2, grid_height / 2)
    
    img_file = os.path.join(current_dir, "images", "menu_image.png")
    img_center_x = (grid_width + 4.5) / 2
    img_center_y = grid_height - 4
    image_to_display = Picture(img_file)
    stddraw.picture(image_to_display, img_center_x, img_center_y)
    
    button_w, button_h = grid_width - 1.5, 2
    button_spacing = 3
    button_x = img_center_x - button_w / 2
    start_y = grid_height - 10
    
    easy_button_file = os.path.join(current_dir, "images", "easy_button.png")
    medium_button_file = os.path.join(current_dir, "images", "medium_button.png")
    hard_button_file = os.path.join(current_dir, "images", "hard_button.png")
    exit_button_file = os.path.join(current_dir, "images", "exit_button.png")
    
    easy_button_image = Picture(easy_button_file)
    medium_button_image = Picture(medium_button_file)
    hard_button_image = Picture(hard_button_file)
    exit_button_image = Picture(exit_button_file)
    
    buttons = [
        ("EASY", start_y),
        ("MEDIUM", start_y - button_spacing),
        ("HARD", start_y - 2 * button_spacing),
        ("EXIT", start_y - 3 * button_spacing)
    ]
    
    for text, y_pos in buttons:
        if text == "EASY":
            stddraw.picture(easy_button_image, img_center_x, y_pos + button_h / 2)
        elif text == "MEDIUM":
            stddraw.picture(medium_button_image, img_center_x, y_pos + button_h / 2)
        elif text == "HARD":
            stddraw.picture(hard_button_image, img_center_x, y_pos + button_h / 2)
        elif text == "EXIT":
            stddraw.picture(exit_button_image, img_center_x, y_pos + button_h / 2)
    
    while True:
        stddraw.show(50)
        if stddraw.mousePressed():
            mouse_x, mouse_y = stddraw.mouseX(), stddraw.mouseY()
            if button_x <= mouse_x <= button_x + button_w:
                for text, y_pos in buttons:
                    if y_pos <= mouse_y <= y_pos + button_h:
                        global game_speed
                        if text == "EASY":
                            game_speed = 80
                            return
                        elif text == "MEDIUM":
                            game_speed = 40
                            return
                        elif text == "HARD":
                            game_speed = 20
                            return
                        elif text == "EXIT":
                            sys.exit()


if __name__ == '__main__':
    start()


def merge_tiles(self, row):
    col = self.grid_width - 1
    while col > 0:
        if self.tile_matrix[row][col] is not None and self.tile_matrix[row][col - 1] is not None:
            if self.tile_matrix[row][col].number == self.tile_matrix[row][col - 1].number:
                new_number = self.tile_matrix[row][col].number * 2
                merged_tile = Tile(self.tile_matrix[row][col].type)
                merged_tile.number = new_number
                self.tile_matrix[row][col] = merged_tile
                self.tile_matrix[row][col - 1] = None
                self.current_score += new_number
                self.shift_tiles_left(row, col - 1)
                continue
        col -= 1


def shift_tiles_left(self, row, start_col):
    for col in range(start_col, self.grid_width - 1):
        if self.tile_matrix[row][col] is None:
            next_tile = None
            next_col = col + 1
            while next_col < self.grid_width:
                if self.tile_matrix[row][next_col] is not None:
                    next_tile = self.tile_matrix[row][next_col]
                    self.tile_matrix[row][next_col] = None
                    break
                next_col += 1
            if next_tile is not None:
                self.tile_matrix[row][col] = next_tile


def get_color_for_number(self):
    color_map = {
        2: Color(238, 228, 218),
        4: Color(237, 224, 200),
        8: Color(242, 177, 121),
        16: Color(245, 149, 99),
        32: Color(246, 124, 95),
        64: Color(246, 94, 59),
        128: Color(237, 207, 114),
        256: Color(237, 204, 97),
        512: Color(237, 200, 80),
        1024: Color(237, 197, 63),
        2048: Color(237, 194, 46)
    }
    return color_map.get(self.number, Color(238, 228, 218))


def display_win_screen(grid_height, grid_width):
    stddraw.setPenColor(Color(0, 0, 0, 150))
    stddraw.filledRectangle(-0.5, -0.5, grid_width + 5, grid_height)
    
    current_dir = os.path.dirname(os.path.realpath(__file__))
    win_img_file = os.path.join(current_dir, "win_lose_images", "win_villager.png")
    win_image = Picture(win_img_file)
    
    img_center_x = (grid_width + 4.5) / 2
    img_center_y = grid_height / 2
    stddraw.picture(win_image, img_center_x, img_center_y)
    stddraw.show(2000)


def display_lose_screen(grid_height, grid_width):
    stddraw.setPenColor(Color(0, 0, 0, 150))
    stddraw.filledRectangle(-0.5, -0.5, grid_width + 5, grid_height)
    
    current_dir = os.path.dirname(os.path.realpath(__file__))
    lose_img_file = os.path.join(current_dir, "win_lose_images", "lose_villager.png")
    lose_image = Picture(lose_img_file)
    
    img_center_x = (grid_width + 4.5) / 2
    img_center_y = grid_height / 2
    stddraw.picture(lose_image, img_center_x, img_center_y)
    stddraw.show(2000)
