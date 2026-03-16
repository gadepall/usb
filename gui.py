import tkinter as tk
import os
import time
import subprocess

def led_off():
    os.system("sudo ./led 0")

def led_on():
    subprocess.Popen(["sudo", "tee", "/sys/bus/pci/devices/0000:00:14.0/remove"], 
                    stdin=subprocess.PIPE).communicate(b"1")
    time.sleep(1)
    subprocess.Popen(["sudo", "tee", "/sys/bus/pci/rescan"], 
                    stdin=subprocess.PIPE).communicate(b"1")

os.system("sudo dmesg -n 1")
os.system("sudo -v")

root = tk.Tk()
root.attributes('-topmost', True)
root.geometry("300x150")

tk.Button(root, text="LED OFF", command=led_off, bg="red", width=20, height=3).pack(pady=5)
tk.Button(root, text="LED ON", command=led_on, bg="green", width=20, height=3).pack(pady=5)

root.mainloop()
