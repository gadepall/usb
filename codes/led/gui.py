import tkinter as tk
import os
import time
import subprocess
import threading

PCI_ADDR = "0000:00:14.0"

def led_off():
    os.system("sudo ./led 0")

def led_on():
    subprocess.Popen(["sudo", "tee", f"/sys/bus/pci/devices/{PCI_ADDR}/remove"],
                    stdin=subprocess.PIPE).communicate(b"1")
    time.sleep(1)
    subprocess.Popen(["sudo", "tee", "/sys/bus/pci/rescan"],
                    stdin=subprocess.PIPE).communicate(b"1")

blinking = False

def blink():
    global blinking
    while blinking:
        led_off()
        time.sleep(2)
        led_on()
        time.sleep(0.25)

def start_blink():
    global blinking
    blinking = True
    t = threading.Thread(target=blink)
    t.daemon = True
    t.start()

def stop_blink():
    global blinking
    blinking = False

os.system("sudo dmesg -n 1")
os.system("sudo -v")

root = tk.Tk()
root.attributes('-topmost', True)
root.geometry("300x250")
root.title("USB LED Controller")

tk.Button(root, text="LED OFF", command=led_off, bg="red", width=20, height=3).pack(pady=5)
tk.Button(root, text="LED ON", command=led_on, bg="green", width=20, height=3).pack(pady=5)
tk.Button(root, text="BLINK", command=start_blink, bg="yellow", width=20, height=3).pack(pady=5)
tk.Button(root, text="STOP BLINK", command=stop_blink, bg="gray", width=20, height=3).pack(pady=5)

root.mainloop()
