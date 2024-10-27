from PIL import Image
from math import sqrt
from pynput.mouse import Button, Controller
from pynput.keyboard import Listener, Key
import time
import pyautogui
import requests
import sys

URL = "https://www.francetvinfo.fr/pictures/uCohbDFuRIFU83JQFWbeVAfxbMg/0x0:634x357/1500x843/2016/08/23/bowserdef.jpg"
CLICK_RATIO = 1 / 500
CURSOR_SIZE = 2

mouse = Controller()

COLORS_TO_POSITION = {
    (0, 0, 0): (499, 395),
    (102, 102, 102): (550, 394),
    (204, 204, 204): (558, 443),
    (255, 0, 0): (556, 545),
    (255, 128, 0): (596, 547),
    (255, 255, 0): (507, 644),
    (128, 255, 0): (505, 539),
    (0, 153, 0): (498, 497),
    (0, 255, 255): (604, 442),
    (0, 0, 255): (600, 401),
    (128, 0, 255): (553, 599),
    (255, 0, 255): (558, 634),
    (102, 51, 0): (600, 502),
    (204, 153, 102): (503, 594),
    (255, 178, 102): (512, 648),
    (255, 204, 204): (593, 648),
    (153, 0, 0): (562, 497),
    (255, 255, 255): (507, 447)
}

COLORS = list(COLORS_TO_POSITION.keys())

def click():
    mouse.click(Button.left)
    time.sleep(CLICK_RATIO)

def press():
    mouse.press(Button.left)
    time.sleep(CLICK_RATIO)

def release():
    mouse.release(Button.left)
    time.sleep(CLICK_RATIO)

def move(position):
    mouse.position = position
    time.sleep(CLICK_RATIO)

def capture_click_positions():
    click_positions = []
    print("Please click anywhere on the screen to capture positions.")
    for i in range(2):
        input(f"Press Enter to capture position {i + 1}...")
        x, y = pyautogui.position()
        click_positions.append((x, y))
        print(f"Position {i + 1} captured at ({x}, {y})")
        time.sleep(0.5)
    return click_positions

def calculate_dimensions(pos1, pos2):
    initial_x, initial_y = pos1
    size_x = pos2[0] - initial_x
    size_y = pos2[1] - initial_y
    return initial_x, initial_y, size_x, size_y

def load_and_resize_image(url, new_size):
    img = Image.open(requests.get(url, stream=True).raw)
    return img.resize(new_size)

def draw_image_from_stored_colors(color_positions, initial_x, initial_y, img):
    for color, positions in color_positions.items():
        position_on_screen = COLORS_TO_POSITION.get(color)

        if position_on_screen:
            move(position_on_screen)
            click()  # Click to select the color

            for (x, y) in positions:
                move((initial_x + x * CURSOR_SIZE, initial_y + y * CURSOR_SIZE))
                click()

def closest_color(rgb):
    r, g, b = rgb
    color_diffs = []
    for color in COLORS:
        cr, cg, cb = color
        color_diff = sqrt((r - cr) ** 2 + (g - cg)**2 + (b - cb)**2)
        color_diffs.append((color_diff, color))
    return min(color_diffs)[1]

def store_pixels_by_color(img):
    color_positions = {}

    for y in range(img.height):
            for x in range(img.width):
                color = closest_color(img.getpixel((x, y)))

                if str(color) == '(255, 255, 255)':
                    continue

                if color not in color_positions:
                    color_positions[color] = []

                color_positions[color].append((x, y))

    return color_positions

def on_press(key):
    try:
        if key == Key.esc:
            print("Escape key pressed, exiting...")
            sys.exit()
    except AttributeError:
        pass

def main():

    listener = Listener(on_press=on_press)
    listener.start()


    click_positions = capture_click_positions()
    initial_x, initial_y, size_x, size_y = calculate_dimensions(*click_positions)
    
    img = load_and_resize_image(URL, (int(size_x / CURSOR_SIZE), int(size_y / CURSOR_SIZE)))

    color_positions = store_pixels_by_color(img)

    time.sleep(5)

    draw_image_from_stored_colors(color_positions, initial_x, initial_y, img)

if __name__ == "__main__":
    main()
