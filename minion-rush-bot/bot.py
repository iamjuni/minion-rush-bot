import pyautogui
import cv2
import numpy as np
import time

# --- CONFIG ---
WAYDROID_REGION = (100, 100, 720, 1280)  # Your Waydroid screen coords
CHECK_INTERVAL = 0.3
MATCH_THRESHOLD = 0.7

# --- Define templates and actions ---
# Each entry is (filename, action_function)
OBSTACLE_TEMPLATES = [
    ('obstacle.png', 'jump'),
    ('obstacle2.png', 'slide'),
    ('obstacle3.png', 'slide'),
    ('obstacle4.png', 'move_right'),
]

# --- Screen capture ---
def capture_screen():
    screenshot = pyautogui.screenshot(region=WAYDROID_REGION)
    frame = cv2.cvtColor(np.array(screenshot), cv2.COLOR_RGB2BGR)
    return frame

# --- Template matching ---
def find_template(frame, template_path, threshold=0.7):
    template = cv2.imread(template_path, 0)
    if template is None:
        print(f"Template not found: {template_path}")
        return False, None
    gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    result = cv2.matchTemplate(gray_frame, template, cv2.TM_CCOEFF_NORMED)
    _, max_val, _, max_loc = cv2.minMaxLoc(result)
    return (max_val >= threshold), max_loc if max_val >= threshold else None

# --- Actions (swipes) ---
def swipe(start, end, duration=0.2):
    pyautogui.moveTo(*start)
    pyautogui.dragTo(*end, duration=duration)

def jump():
    print("🟡 Jumping!")
    cx = WAYDROID_REGION[0] + WAYDROID_REGION[2] // 2
    swipe((cx, 1000), (cx, 700))

def slide():
    print("🔵 Sliding!")
    cx = WAYDROID_REGION[0] + WAYDROID_REGION[2] // 2
    swipe((cx, 700), (cx, 1000))

def move_left():
    print("🟣 Moving Left!")
    y = WAYDROID_REGION[1] + 900
    swipe((WAYDROID_REGION[0] + 500, y), (WAYDROID_REGION[0] + 200, y))

def move_right():
    print("🟢 Moving Right!")
    y = WAYDROID_REGION[1] + 900
    swipe((WAYDROID_REGION[0] + 200, y), (WAYDROID_REGION[0] + 500, y))

# --- Action lookup ---
ACTIONS = {
    'jump': jump,
    'slide': slide,
    'move_left': move_left,
    'move_right': move_right
}

# --- Main loop ---
print("🤖 Multi-obstacle bot running. Press Ctrl+C to stop.")

try:
    while True:
        frame = capture_screen()

        for template_file, action_name in OBSTACLE_TEMPLATES:
            found, location = find_template(frame, template_file, MATCH_THRESHOLD)
            if found:
                print(f"⚠️ Detected {template_file} at {location} -> {action_name}")
                ACTIONS[action_name]()  # call the correct function
                break  # only react to one at a time

        time.sleep(CHECK_INTERVAL)

except KeyboardInterrupt:
    print("🛑 Bot stopped.")
