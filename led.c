#include <stdio.h>
#include <stdlib.h>
#include <libusb-1.0/libusb.h>

int main(int argc, char *argv[]) {
    if (argc != 2) return 1;
    libusb_init(NULL);
    libusb_device_handle *dev_handle = libusb_open_device_with_vid_pid(NULL, 0x1d6b, 0x0002); 
    if (!dev_handle) return 1;

    int port_number = 9;
    int wIndex_test = (3 << 8) | port_number; 
    libusb_control_transfer(dev_handle, 0x23, 0x03, 21, wIndex_test, NULL, 0, 1000);
    
    libusb_close(dev_handle);
    libusb_exit(NULL);
    return 0;
}
