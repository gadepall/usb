all:
	gcc display.c -o display -lusb-1.0

run:
	xhost +local:
	sudo -v
	sudo -E python3 gui.py
