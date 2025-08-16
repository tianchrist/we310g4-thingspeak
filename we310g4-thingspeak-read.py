"""
we310g4-thingspeak-read.py

Description:
    Example Python script to read data from Thingspeak using TCP transfer 
    in Telit WE310G4 module.

Usage:
    python we310g4-thingspeak-read.py

Author: tianchrist
Date: 2025-08-11
"""

import serial, time
from we310g4Test import send_at_command, receive_response
from mycredentials import *

def main():
    port = '/dev/tty.usbserial-FTL83DL1'  # Replace with your serial port
    baudrate = 115200
    with serial.Serial(port, baudrate, timeout=1) as ser:
        # send_at_command(ser,'AT+YSR\r\n')
        # send_at_command(ser,'AT+YSR\r\n')
        # time.sleep(1)
        # response = receive_response(ser)
        # print("Response:")
        # print(response)
        
        send_at_command(ser,'AT\r\n')
        # first AT after reset will return "INVALID COMMAND" but it is ok
        send_at_command(ser,'AT\r\n')
        response = receive_response(ser)
        print(response)

        # Enable station mode
        # command = 'AT+WNI=0\r\n'
        # send_at_command(ser, command)
        # response = receive_response(ser)
        # print(response)

        # Connect to Wi-Fi network
        command=f'at+wncn=1,"{SSID}","{PASSWORD}"\r\n'
        print(command)
        # send_at_command(ser, command)
        # time.sleep(10)
        # response = receive_response(ser)
        # print(response)

        command='AT+WNIFCFG\r\n'
        send_at_command(ser, command)
        response = receive_response(ser)
        print(response)

        command='AT+NDNSCRURL="api.thingspeak.com"\r\n'
        send_at_command(ser, command)
        response = receive_response(ser)
        print(response)

if __name__ == "__main__":
    main()