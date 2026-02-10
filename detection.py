import cv2
import numpy as np
import mss


class ScreenDetector:
    def __init__(self):
        self.sct = mss.mss()

    def __call__(self, images, region, conf=70):
        # Handle single string by converting to list
        if isinstance(images, str):
            images = [images]
        elif not isinstance(images, (list, tuple)):
            raise ValueError("images must be a string, list, or tuple of image paths")

        # Define the monitor region for MSS (left, top, width, height)
        mon = {"left": region[0], "top": region[1], "width": region[2], "height": region[3]}

        screen = self.sct.grab(mon)
        screen_cv = cv2.cvtColor(np.array(screen), cv2.COLOR_BGRA2BGR)  # MSS returns BGRA

        conf_threshold = conf / 100.0

        for img_path in images:
            template = cv2.imread(img_path, cv2.IMREAD_COLOR)
            if template is None:
                print(f"Warning: Failed to load image '{img_path}' - check path and file existence")
                continue

            # Ensure template is not larger than screen region
            if template.shape[0] > screen_cv.shape[0] or template.shape[1] > screen_cv.shape[1]:
                continue

            res = cv2.matchTemplate(screen_cv, template, cv2.TM_CCOEFF_NORMED)
            min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)

            # Return True and the top-left location relative to the region
            if max_val >= conf_threshold:
                return True, max_loc

        return False, None
