import serial
import time

def read_file_to_string(filepath):
    """
    Reads the entire content of a file into a string.
    :param filepath: Path to the file
    :return: File content as a string
    """
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    return content

def send_at_command(ser, command, delay=0.1):
    """
    Sends an AT command to the serial port.
    :param ser: An open serial.Serial object
    :param command: AT command to send (e.g., 'AT\r\n')
    """
    ser.write(command.encode())
    time.sleep(delay)  # Wait for the device to process the command

def receive_response(ser, timeout=1):
    """
    Reads the response from the serial port.
    :param ser: An open serial.Serial object
    :param timeout: Timeout for reading the response (in seconds)
    :return: Response from the device
    """
    ser.timeout = timeout
    response = ser.read_all().decode('utf-8')
    return response

def receive_full_response(ser, poll_interval=0.1, max_idle=1):
    """
    Polls the serial port until no more incoming data is received.
    :param ser: An open serial.Serial object
    :param poll_interval: Time (seconds) to wait between polls
    :param max_idle: Time (seconds) to wait with no data before stopping
    :return: Full response as a string
    """
    response = b""
    idle_time = 0
    while True:
        data = ser.read_all()
        if data:
            response += data
            idle_time = 0
        else:
            time.sleep(poll_interval)
            idle_time += poll_interval
            if idle_time >= max_idle:
                break
    return response.decode('utf-8', errors='ignore')

def we310g4_soft_reset(ser):
    """
    Function to reset the WE310G4 module using AT command.
    :param ser: An open serial.Serial object
    """
    send_at_command(ser,'AT+YSR\r\n')
    time.sleep(1)
    response = receive_full_response(ser, 0.1, 2)

if __name__ == "__main__":
    port = '/dev/tty.usbserial-FTL83DL1'  # Replace with your serial port
    baudrate = 115200
    initcommandList = [
        'AT\r\n',
        'ATE1\r\n',
        'AT+CGMR\r\n',
        'AT+CGMM\r\n',
        'at+wni=0\r\n',
    ]

    try:
        with serial.Serial(port, baudrate, timeout=1) as ser:
            for command in initcommandList:
                send_at_command(ser, command)
                response = receive_response(ser)
                print(f"Command: {command.strip()}")
                print("Response:")
                print(response)

            # command = 'at+wncn=1,"",""\r\n'
            # print(f"Command: {command.strip()}")
            # send_at_command(ser, command)
            # time.sleep(2)
            # response = receive_full_response(ser,0.1, 5)
            # print("Response:")
            # print(response)

            command = 'AT+WNCN?\r\n'
            send_at_command(ser, command)
            response = receive_response(ser)
            print(f"Command: {command.strip()}")
            print("Response:")
            print(response)

            httpsCommandList = [
                'AT+NSSLCERTLIST=0\r\n',
              #  'AT+NHTTPCINIT=1,100,1440,1440,1440\r\n',
            ]

            for command in httpsCommandList:
                send_at_command(ser, command)
                response = receive_response(ser)
                print(f"Command: {command.strip()}")
                print("Response:")
                print(response)

            certFile = read_file_to_string('www-filesampleshub-com.pem')
            print(len(certFile))
            #print(certFile)

            command = 'AT+NSSLCERTSTORE=0,1,1,"ca",1854,'
            send_at_command(ser, command, delay=0.02)
            send_at_command(ser, certFile)
            response = receive_full_response(ser,0.1, 3)
            print("Response:")
            print(response)
        
    except serial.SerialException as e:
        print(f"Error: {e}")
