#include <stdio.h>
#include <stdlib.h>
#include <libusb-1.0/libusb.h>
#include <unistd.h>

const int digits[10][7] = {
    {1, 0, 0, 0, 0, 0, 0},
    {1, 1, 1, 1, 0, 0, 1},
    {0, 1, 0, 0, 1, 0, 0},
    {0, 1, 1, 0, 0, 0, 0},
    {0, 0, 1, 1, 0, 0, 1},
    {0, 0, 1, 0, 0, 1, 0},
    {0, 0, 0, 0, 0, 1, 0},
    {1, 1, 1, 1, 0, 0, 0},
    {0, 0, 0, 0, 0, 0, 0},
    {0, 0, 1, 0, 0, 0, 0}
};

void set_test_mode(libusb_device_handle *dev, int port, int mode) {
    int wIndex = (mode << 8) | port;
    libusb_control_transfer(dev, 0x23, 0x03, 21, wIndex, NULL, 0, 1000);
}

int main(int argc, char *argv[]) {
    if (argc != 2) return 1;

    int number = atoi(argv[1]);
    if (number < 0 || number > 9) return 1;

    int port_number = 9;

    libusb_init(NULL);

    libusb_device_handle *dev_handle =
        libusb_open_device_with_vid_pid(NULL, 0x1d6b, 0x0002);
    if (!dev_handle) return 1;

    for (int i = 0; i < 7; i++) {
        int bit = digits[number][i];

        if (bit == 0) {
            set_test_mode(dev_handle, port_number, 3);
            usleep(300000);
            set_test_mode(dev_handle, port_number, 2);
            usleep(50000);
        } else {
            set_test_mode(dev_handle, port_number, 1);
            usleep(300000);
            set_test_mode(dev_handle, port_number, 2);
            usleep(50000);
        }
    }

    libusb_close(dev_handle);
    libusb_exit(NULL);
    return 0;
}
