import tkinter as tk
import os
import time
import subprocess

PCI_ADDR = "0000:00:14.0"

def display_digit():
    num = entry.get()
    if num.isdigit() and 0 <= int(num) <= 9:
        os.system(f"sudo ./display {num}")

def reset():
    subprocess.Popen(["sudo", "tee", f"/sys/bus/pci/devices/{PCI_ADDR}/remove"],
                    stdin=subprocess.PIPE).communicate(b"1")
    time.sleep(1)
    subprocess.Popen(["sudo", "tee", "/sys/bus/pci/rescan"],
                    stdin=subprocess.PIPE).communicate(b"1")

os.system("sudo dmesg -n 1")
os.system("sudo -v")

root = tk.Tk()
root.attributes('-topmost', True)
root.geometry("300x200")
root.title("Seven Segment Display")

entry = tk.Entry(root, font=("Arial", 24), width=5, justify='center')
entry.pack(pady=10)

tk.Button(root, text="DISPLAY", command=display_digit, bg="blue", fg="white", width=20, height=3).pack(pady=5)
tk.Button(root, text="RESET", command=reset, bg="gray", width=20, height=3).pack(pady=5)

root.mainloop()
