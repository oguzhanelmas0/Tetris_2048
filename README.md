# Tetris_2048
A Python-based game combining mechanics from Tetris and 2048

# Tetris 2048 – Minecraft Themed Edition

**Tetris 2048** is a unique Python game project that blends the classic **Tetris** mechanics with the addictive tile-merging logic of **2048**, all wrapped in a fun **Minecraft-themed** visual design.

## 🎮 Game Features

- **Three Game Modes**: Choose from Easy, Medium, or Hard — each with different falling speeds to challenge your reflexes.
- **Minecraft Theme**: The game interface, buttons, and visual elements are styled with a Minecraft aesthetic to attract a broad audience of casual and young gamers.
- **Tile Merging**: Like 2048, when two tiles with the same number collide, they merge into one with their sum.
- **Floating Tile Handling**: The game includes a physics-inspired mechanic to eliminate floating tiles after merges.
- **Ghost Piece Support**: You can see a grey shadow of where the Tetromino will land.
- **Pause Menu**: Press `ESC` during gameplay to open a pause menu where you can resume, restart, or exit the game.

## 🕹 Controls

- **← / → / ↓**: Move the Tetromino left, right, or down
- **↑**: Rotate clockwise
- **Z**: Rotate counter-clockwise
- **ESC**: Open Pause Menu

## 📁 Project Structure

- `Tetris_2048.py` – Main execution script
- `game_grid.py` – Grid logic including merge and gravity
- `tetromino.py` – Tetromino behavior and rotation
- `tile.py` – Tile rendering and color assignment
- `lib/stddraw.py`, `lib/color.py`, `lib/picture.py` – GUI and rendering support
- `images/` – Button and background graphics
- `sounds/` – Background music
- `menu_images/`, `win_lose_images/` – In-game menus and result screens

## ✅ Requirements

- Python 3.8+
- `pygame` library (for GUI rendering)
- `playsound` library (for audio playback)

---

Enjoy the game and feel free to fork and enhance it!

