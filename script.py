from PIL import Image
from math import sqrt
from pynput.mouse import Button, Controller
import time
import pyautogui
import requests

URL = "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQhRfwVmHnOt0p7zNSYNhfWkYrkuFiTP7iTWQ&s"
CLICK_RATIO = 1 / 15000
CURSOR_SIZE = 1

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
    (153, 0, 0): (562, 497)
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

def closest_color(rgb):
    return min(COLORS, key=lambda color: sqrt(sum((c1 - c2) ** 2 for c1, c2 in zip(rgb, color))))

def load_and_resize_image(url, new_size):
    img = Image.open(requests.get(url, stream=True).raw)
    return img.resize(new_size)

def draw_image_from_colors(img, initial_x, initial_y):
    for color, position in COLORS_TO_POSITION.items():
        move(position)
        click()
        dx, dy = initial_x, initial_y

        for y in range(img.height):
            for x in range(img.width):
                pixel = closest_color(img.getpixel((x, y)))
                if pixel == color and pixel != (255, 255, 255):
                    move((dx, dy))
                    press()
                else:
                    release()
                dx += CURSOR_SIZE
            dy += CURSOR_SIZE
            dx = initial_x

def main():
    click_positions = capture_click_positions()
    initial_x, initial_y, size_x, size_y = calculate_dimensions(*click_positions)
    
    img = load_and_resize_image(URL, (int(size_x / CURSOR_SIZE), int(size_y / CURSOR_SIZE)))
    draw_image_from_colors(img, initial_x, initial_y)

if __name__ == "__main__":
    main()
