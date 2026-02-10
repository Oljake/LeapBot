import random
import pyautogui


class ScreenClicker:
    def __init__(self):
        pass

    def __call__(self, region: list, click_type: str = 'left', move_duration: bool | tuple = False, debug: bool = False):

        if len(region) == 4:
            x: float = random.uniform(region[0], region[2])
            y: float = random.uniform(region[1], region[3])
        else:
            x, y = region

        # Determine move duration
        duration: float = random.uniform(move_duration[0], move_duration[1]) if move_duration else 0.0

        # Perform the move with integrated duration (fixed: use moveTo for absolute positioning)
        pyautogui.moveTo(x, y, duration=duration)

        # Perform the click
        pyautogui.click(x=x, y=y, button=click_type)

        if debug:
            print(f"{click_type.capitalize()} click @ ({x}, {y})")
