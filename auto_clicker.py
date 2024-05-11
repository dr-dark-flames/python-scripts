import time
import threading
from random import random
from pynput import mouse
from elevate import elevate

elevate()

toggle_key = "Button.x1"
delay = 0.03
clicking = False
auto_mouse = mouse.Controller()


def clicker():
    while True:
        if clicking:
            auto_mouse.click(mouse.Button.right)
        time.sleep(delay * random() + 1 / 2 * delay)


def toggle(x, y, button, pressed):
    global clicking
    if str(button) == toggle_key:
        print('{0} at {1}'.format(
            'Pressed' if pressed else 'Released',
            (x, y)))
        clicking = not clicking


if __name__ == '__main__':
    click_thread = threading.Thread(target=clicker)
    click_thread.start()

    with mouse.Listener(on_click=toggle) as listener:
        try:
            listener.join()
        except Exception as e:
            print('{0} was clicked'.format(e.args[0]))
