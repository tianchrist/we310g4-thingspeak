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
from we310g4Test import *
from mycredentials import *

def parse_response_keyword(response,keyword):
    """
    Parses the response to find a specific keyword and returns the value after it.
    Args:
        response (str): The response string to parse.
        keyword (str): The keyword to search for in the response.
    Returns:
        str: The value found after the keyword, or an empty string if not found.    
    """
    # Example implementation: find the keyword and return the value after it
    if keyword in response:
        parts = response.split(keyword)
        if len(parts) > 1:
            return parts[1].strip().split()[0][1:] # [1:] remove leading colon
    return ""
   
def find_line_keyword(response, keyword):
    """
    Finds a line in a multi-line response that contains a specific keyword.
    Args:
        response (str): The multi-line response string to search.
        keyword (str): The keyword to search for in the response.
    Returns:
        str: The first line containing the keyword, or an empty string if not found.
    """
    lstResponse = response.replace('\n', ',').replace('\r', '').split(',')
    for item in lstResponse:
        if keyword in item:
            return item.strip()
    return ""

def wifi_is_up(ser):
    """
    Function to check if Wi-Fi is up.
    :param ser: An open serial.Serial object
    :return: bool: True if Wi-Fi is up, False otherwise.
    """
    command='AT+WNIFCFG\r\n'
    send_at_command(ser, command)
    response = receive_response(ser)
    #print(response)
    lines = response.splitlines()
    #print(lines)
    for line in lines:
        if 'UP' in line:
            return True
    return False

def wifi_connect(ser,whandle,ssid,password):
    """
    Function to connect to a Wi-Fi network.
    :param ser: An open serial.Serial object
    :param ssid: SSID of the Wi-Fi network
    :param password: Password of the Wi-Fi network
    :return: None
    """
#        print(f'Connecting to SSID: {ssid} with PASSWORD: {password}')
    command=f'at+wncn={whandle},"{ssid}","{password}"\r\n'
#    print(command)
    send_at_command(ser, command)
    time.sleep(2)
    response = receive_full_response(ser,0.5,5)
    #print(response)

def main():
    port = '/dev/tty.usbserial-FTL83DL1'  # Replace with your serial port
    baudrate = 115200
    with serial.Serial(port, baudrate, timeout=1) as ser:
        #we310g4_soft_reset(ser)
        
        send_at_command(ser,'AT\r\n')
        # first AT after reset will return "INVALID COMMAND" but it is ok
        send_at_command(ser,'AT\r\n')
        response = receive_response(ser)
        print(response)

        # Enable station mode
        command = 'AT+WNI=0\r\n'
        send_at_command(ser, command)
        response = receive_full_response(ser)
        print(response)
        response=find_line_keyword(response, '+WNI:')
        print(response)
        whandle= parse_response_keyword(response, '+WNI')
        print(f'WNI handle: {whandle}') 
        attempts=3
        while (attempts > 0) and (not wifi_is_up(ser)):
            print(f'Attempting to connect to Wi-Fi, attempts left: {attempts}')
            wifi_connect(ser,whandle,SSID,PASSWORD)
            attempts -= 1
            time.sleep(2)

        if wifi_is_up(ser):
            print('Wi-Fi is up!')
        else:
            print('Failed to connect to Wi-Fi.')
            return             

        command='AT+NDNSCRURL="api.thingspeak.com"\r\n'
        send_at_command(ser, command)
        response = receive_full_response(ser, 0.1, 1)
        print(response)
        print('Resolving Thingspeak IP...')
        # remove linebreaks and replace with commas
        strResponse = response.replace('\n', ',').replace('\r', '')
        #print(f'replace linebreak by comma:{strResponse}')
        lstResponse=strResponse.split(',')
        lstResponse=[item for item in lstResponse if item != ''] 
        #print(f'split at comma:{lstResponse}')        
        thingspeakIP=lstResponse[1].split(':')[1]
        print(f'Thingspeak IP: {thingspeakIP}')


        # open TCP connection
        command='AT+SC=2,1,0\r\n'
        send_at_command(ser, command)
        response = receive_response(ser)
        response=find_line_keyword(response, '+SC:')
        cid= parse_response_keyword(response, '+SC')
        print(f'CID: {cid}')


if __name__ == "__main__":
    main()