# You import all the IOs of your board
import board
import busio

# These are imports from the kmk library
from kmk.kmk_keyboard import KMKKeyboard
from kmk.scanners.keypad import MatrixScanner
from kmk.keys import KC
from kmk.modules.layers import Layers
from kmk.modules.macros import Press, Release, Tap, Macros

# OLED Display imports
from kmk.extensions.display import Display, TextEntry
from kmk.extensions.display.ssd1306 import SSD1306

# This is the main instance of your keyboard
keyboard = KMKKeyboard()

# Add the macro extension
macros = Macros()
keyboard.modules.append(macros)

# Add layers support
layers = Layers()
keyboard.modules.append(layers)

# Setup I2C for OLED (using SDA and SCL pins)
i2c_bus = busio.I2C(scl=board.SCL, sda=board.SDA)

# Initialize the OLED display (128x32, I2C address usually 0x3C)
oled_display = SSD1306(
    i2c=i2c_bus,
    device_address=0x3C,
)

# Create display extension
display = Display(
    display=oled_display,
    width=128,
    height=32,
    flip=False,
)

# Add text to display
display.entries = [
    TextEntry(text='BO55 MACROPAD', x=0, y=0, x_anchor='L', y_anchor='T'),
    TextEntry(text='SETTING ONE', x=0, y=16, x_anchor='L', y_anchor='T'),
]

# Add display to keyboard
keyboard.extensions.append(display)

# Define your matrix pins based on the schematic
# Columns: GPIO28/A2, GPIO27/A1, GPIO26/A0, GPIO29/A3
# Rows: GPIO0/TX, GPIO1/RX, GPIO2/D2, GPIO3/D3
COL_PINS = (board.A2, board.A1, board.A0, board.A3)
ROW_PINS = (board.TX, board.RX, board.D2, board.D3)

# Tell kmk we are using a key matrix (4 rows x 4 columns)
keyboard.matrix = MatrixScanner(
    column_pins=COL_PINS,
    row_pins=ROW_PINS,
    columns_to_anodes=False,
)

# Fusion 360 keymap
# Layout:
# [ESC] [L]   [C]   [E]
# [R]   [O]   [M]   [P]
# [S]   [T]   [F]   [X]
# [D]   [UNDO][REDO][SAVE]
keyboard.keymap = [
    [
        # ROW 0 (connected to TX)
        KC.ESC,   KC.L,     KC.C,     KC.E,        # Escape, Line, Circle, Extrude
        # ROW 1 (connected to RX)
        KC.R,     KC.O,     KC.M,     KC.P,        # Rectangle, Offset, Move, Press/Pull
        # ROW 2 (connected to D2)
        KC.S,     KC.T,     KC.F,     KC.X,        # Sketch, Trim, Fillet, Construction
        # ROW 3 (connected to D3)
        KC.D,     KC.LCTL(KC.Z), KC.LCTL(KC.Y), KC.LCTL(KC.S),  # Dimension, Undo, Redo, Save
    ]
]

# Start kmk!
if __name__ == '__main__':
    keyboard.go()