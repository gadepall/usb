all:
	gcc led.c -o led -lusb-1.0

run:
	xhost +local:
	sudo -v
	sudo -E python3 gui.py
