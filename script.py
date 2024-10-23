from PIL import Image
from math import sqrt
from pynput.mouse import Button, Controller
import time

initialX = 900
initialY = 400

dx = initialX
dy = initialY

cursorSize = 1

def mouseClick():
    mouse = Controller()
    mouse.click(Button.left)
    time.sleep(1/1000)

def mousePress():
     mouse = Controller()
     mouse.press(Button.left)
     time.sleep(1/1000)

def mouseRelease():
    mouse = Controller()
    mouse.release(Button.left)
    time.sleep(1/1000)

def moveMouse(pos):
     mouse = Controller()
     mouse.position = pos
     time.sleep(1/1000)

def getMousePosition():
     mouse = Controller()
     return mouse.position

moveMouse((dx, dy));

COLORS_TO_POSITION = {
    (0,0,0): (568 , 85),
    (105, 105, 105): (600, 85),
    (255, 0, 0): (625, 85),
    (255, 165, 0): (675, 85),
    (255, 255, 0): (700, 85),
    (0, 255, 0): (720, 85),
    (0, 0, 255): (770, 85),
    (128, 0, 128): (790, 85),
    (255, 255, 255): (568, 110),
    (211, 211, 211): (600, 110),
    (139, 69, 19): (620, 110),
    (255, 192, 203): (640, 110)
}

def getColorPosition(rgb):
    return COLORS_TO_POSITION.get(rgb, "Unknown Color");

img = Image.open("C:\\Users\\antoi\\Downloads\\18904134-portrait-de-chien-noir-et-blanc-illustration-de-visage-de-chien-illustration-d-animal-de-compagnie-vectoriel.jpg")
px = img.load();

img = img.resize((int(300 / cursorSize), int(300 / cursorSize)));

COLORS = [
    (0, 0, 0),       # Noir
    (255, 255, 255), # Blanc
    (255, 0, 0),     # Rouge
    (0, 0, 255),     # Bleu
    (255, 255, 0),   # Jaune
    (0, 255, 0),     # Vert
    (255, 165, 0),   # Orange
    (255, 192, 203), # Rose
    (128, 0, 128),   # Violet
    (139, 69, 19),   # Marron
    (211, 211, 211), # Gris clair
    (105, 105, 105)  # Gris foncé
]

def closest_color(rgb):
    r, g, b = rgb
    color_diffs = []
    for color in COLORS:
        cr, cg, cb = color
        color_diff = sqrt((r - cr) ** 2 + (g - cg)**2 + (b - cb)**2)
        color_diffs.append((color_diff, color))
    return min(color_diffs)[1]

for y in range(img.height):
        for x in range(img.width):
            pixel = closest_color(img.getpixel((x, y)))
            if str(pixel) != '(255, 255, 255)':
                moveMouse((dx, dy))
                mousePress()
            else:
                 mouseRelease()
                 
            dx += cursorSize
        dy += cursorSize
        dx = initialX