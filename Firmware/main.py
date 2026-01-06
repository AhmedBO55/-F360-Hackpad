import board
import busio
from kmk.kmk_keyboard import KMKKeyboard
from kmk.scanners.keypad import MatrixScanner
from kmk.keys import KC
from kmk.modules.layers import Layers
from kmk.modules.macros import Press, Release, Tap, Macros
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

# Define layers
# Layer 0: Fusion 360 shortcuts
# Layer 1: Numbers and symbols (activated by holding bottom-right key)
keyboard.keymap = [
    # LAYER 0 - Fusion 360 shortcuts
    # Layout:
    # [ESC] [L]   [C]   [E]
    # [R]   [O]   [M]   [P]
    # [S]   [T]   [F]   [X]
    # [D]   [UNDO][REDO][LAYER]
    [
        # ROW 0 (connected to TX)
        KC.ESC,   KC.L,     KC.C,     KC.E,        # Escape, Line, Circle, Extrude
        # ROW 1 (connected to RX)
        KC.R,     KC.O,     KC.M,     KC.P,        # Rectangle, Offset, Move, Press/Pull
        # ROW 2 (connected to D2)
        KC.S,     KC.T,     KC.F,     KC.X,        # Sketch, Trim, Fillet, Construction
        # ROW 3 (connected to D3)
        KC.D,     KC.LCTL(KC.Z), KC.LCTL(KC.Y), KC.MO(1),  # Dimension, Undo, Redo, Hold for Layer 1
    ],
    
    # LAYER 1 - Numbers and symbols
    # Layout:
    # [1]   [2]   [3]   [+]
    # [4]   [5]   [6]   [-]
    # [7]   [8]   [9]   [*]
    # [0]   [.]   [ENT] [LAYER]
    [
        # ROW 0
        KC.N1,    KC.N2,    KC.N3,    KC.PLUS,     # 1, 2, 3, +
        # ROW 1
        KC.N4,    KC.N5,    KC.N6,    KC.MINS,     # 4, 5, 6, -
        # ROW 2
        KC.N7,    KC.N8,    KC.N9,    KC.ASTR,     # 7, 8, 9, *
        # ROW 3
        KC.N0,    KC.DOT,   KC.ENT,   KC.TRNS,     # 0, ., Enter, (transparent - exits layer)
    ],
]

# Start kmk!
if __name__ == '__main__':
    keyboard.go()
