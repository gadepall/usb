# USB LED & Seven Segment Display Control via D+ Pin Manipulation

Control an LED (and attempt a seven-segment display) using a Linux laptop's USB D+ data pin — no microcontroller, no Arduino, no serial adapter.

**Authors:** Aarush Dilawri, Vivek Darji  
**Institution:** IIT Hyderabad, Department of Electrical Engineering  
**Supervisor:** Dr. GVV Sharma

---

## How It Works

USB 2.0 defines Test Modes that allow software to force the D+ pin to 0V. By building a circuit where the LED depends on D+ voltage, we can turn the LED on and off purely through software.

- **LED OFF:** Send `Test_SE0_NAK` via libusb → D+ forced to 0V → LED turns off
- **LED ON:** PCIe remove + rescan resets the xHCI controller → D+ returns to normal → LED turns on

---

## Requirements

- Linux laptop (tested on Arch Linux with Intel Raptor Lake xHCI)
- Python 3
- libusb-1.0
- tkinter

Install dependencies:
```bash
sudo pacman -S libusb python-tkinter   # Arch
sudo apt install libusb-1.0-0-dev python3-tk  # Ubuntu/Debian
```

---

## Step 1: Find Your PCI Address

```bash
lspci | grep -i usb
```

You'll see something like:
```
00:14.0 USB controller: Intel Corporation xHCI Host Controller
```

Open `led/gui.py` and `sevenseg/gui.py` and update this line with your address:
```python
PCI_ADDR = "0000:00:14.0"
```

---

## Step 2: Find Your USB Port Number

Plug a device into the USB port you want to use, then run:
```bash
lsusb -t
```

Note the port number (e.g. Port 9). Update `port_number` in `led/led.c` and `sevenseg/display.c`:
```c
int port_number = 9;
```

---

## LED Project

### Circuit

```
VBUS (5V) ──── 2.2kΩ ──── D+ ──── LED(anode→cathode) ──── GND
```

Use a micro USB cable. Pin layout:
```
| 1    2    3    4 |
| VCC  D-   D+  GND|
```

### Build and Run

```bash
cd led
make
make run
```

### Controls

| Button | Action |
|---|---|
| LED OFF | Turns LED off via Test_SE0_NAK |
| LED ON | Resets xHCI controller, LED turns back on |
| BLINK | Blinks LED (2s off, 0.25s on) |
| STOP BLINK | Stops blinking |

### Notes

- Keyboard will freeze for ~2 seconds when clicking LED ON — this is normal
- GUI stays on top so you can click LED ON with mouse while keyboard is frozen
- Run `sudo -v` before launching to cache password

---

## Seven Segment Display Project (Experimental)

> **Note:** This project was attempted but the clock signal could not be reliably established via D- due to xHCI test mode transition latency. The code is included for reference.

### Circuit

Uses CD4015 dual 4-bit shift register.

```
VBUS ──── CD4015 VDD (Pin 16)
GND  ──── CD4015 VSS (Pin 8)
GND  ──── Reset A (Pin 6), Reset B (Pin 14)
D-   ──── Clock A (Pin 9), Clock B (Pin 1)
D+   ──── 300Ω ──── Data A (Pin 7) ──── 330µF ──── GND
Q3A (Pin 2) ──── Data B (Pin 15)

CD4015 outputs → 2.2kΩ → Seven segment segments:
Pin 5  (Q0A) → Segment A
Pin 4  (Q1A) → Segment B
Pin 3  (Q2A) → Segment C
Pin 2  (Q3A) → Segment D
Pin 13 (Q0B) → Segment E
Pin 12 (Q1B) → Segment F
Pin 11 (Q2B) → Segment G

COM → VBUS (common anode display)
VBUS ──── 2.2kΩ ──── D+
VBUS ──── 2.2kΩ ──── D-
```

### Build and Run

```bash
cd sevenseg
make
make run
```

Type a digit (0-9) in the box and click DISPLAY. Click RESET after to restore keyboard.

---

## Repo Structure

```
├── led/
│   ├── led.c       # Forces Test_SE0_NAK on USB port
│   ├── gui.py      # Tkinter GUI with ON/OFF/BLINK
│   └── Makefile
├── sevenseg/
│   ├── display.c   # Shifts digit bits into CD4015
│   ├── gui.py      # Tkinter GUI with digit input
│   └── Makefile
└── README.md
```

---

## Troubleshooting

**LED not turning off:**
- Make sure you're running with sudo
- Check resistor value — too low and xHCI can't pull D+ to 0V
- Verify port number matches your actual USB port (`lsusb -t`)

**Permission denied on PCIe reset:**
- Make sure sudo password is cached (`sudo -v` before running)

**GUI not opening (display error):**
- Run `xhost +local:` before `make run`
- Use `sudo -E` to preserve display environment variables

**Keyboard not coming back:**
- Wait 3-5 seconds after clicking LED ON
- If still frozen, the PCIe rescan is still completing
