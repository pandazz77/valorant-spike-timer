import pyautogui
from overlay import Overlay
import threading
from timer import Timer
import time

spike_time = 45
detect_time = 2
confidence = 0.5
overlay = Overlay()
overlay_offset_x = -45
overlay_offset_y = 50


def main():
    spike_timer = Timer(spike_time,name="spike",running_task=overlay.set_label,stop_task=overlay.hide_label)
    spike_timer.running_args=lambda: "%f" % spike_timer.get_remaining_time()
    spike_timer.start()
    was_located = False
    wait_t1 = 0
    while True:
        locate = pyautogui.locateOnScreen("spike.png",confidence=confidence)
        if locate: # object detected on screen
            was_located = True
            x,y,w,h = locate
            print("\rdetected",end="                        ")
            if not spike_timer.running:
                spike_timer.restart()
            else:
                overlay.set_geometry(x+w/2+overlay_offset_x, y+h+overlay_offset_y)
        else:
            print("\rnot detected",end="                    ")
            if was_located:
                wait_t1 = time.time()
                was_located = False
            if wait_t1 and time.time()-wait_t1>=detect_time:
                if spike_timer.running: spike_timer.stop()
                wait_t1 = 0


if __name__ == "__main__":
    thread = threading.Thread(target=main)
    thread.start()
    overlay.loop()
            
