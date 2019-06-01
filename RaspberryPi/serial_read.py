import time
import serial

ser1 = serial.Serial(
    port = '/dev/ttyUSB0',
    baudrate = 9600,
    parity = serial.PARITY_NONE,
    stopbits = serial.STOPBITS_ONE,
    bytesize = serial.EIGHTBITS,
    timeout = 5
    )

ser2 = serial.Serial(
    port = '/dev/ttyUSB1',
    baudrate = 9600,
    parity = serial.PARITY_NONE,
    stopbits = serial.STOPBITS_ONE,
    bytesize = serial.EIGHTBITS,
    timeout = 5
    )

counter1 = 0;
counter2 = 0;

def serial_read():
    global ser1, ser2, counter1, counter2
    for i in range(4):
        data1 = ser1.readline().decode()
        if len(data1) >= 4:
            first = ord(data1[0]) - 64
            second = ord(data1[1]) - 64
            third = ord(data1[2]) - 64
            forth = ord(data1[3]) - 64
            
            counter1 = counter1 + 1
            value1 = str(first) + str(second) + str(third) + str(forth)
            
            if counter1%3 is 1:
                voltage = value1
            elif counter1%3 is 2:
                current = value1
            else:
                power = value1
                counter1 = 0;
    
    for j in range(5):
        data2 = ser2.readline().decode()
        if len(data2) >= 4:
            one = ord(data2[0]) - 64
            two = ord(data2[1]) - 64
            three = ord(data2[2]) - 64
            four = ord(data2[3]) - 64
            
            counter2 = counter2 + 1
            value2 = str(one) + str(two) + str(three) + str(four)
            
            if counter2%4 is 1:
                top = value2
            elif counter2%4 is 2:
                bottom = value2
            elif counter2%4 is 3:
                right = value2
            else:
                left = value2
                counter2 = 0;

    return voltage, current, power, top, bottom, right, left
    
    
while (1):
    
    v, c, p, t, b, r, l = serial_read()

    print("Voltage:\t", v)
    print("Current:\t", c)
    print("Power:\t\t", p)
    print("Top:\t\t", t)
    print("Bottom:\t\t", b)
    print("Right:\t\t", r)
    print("Left:\t\t", l)
    print("\n")


    #print("Voltage:\t", voltage)
    #print("Current:\t", current)
    #print("Power:\t\t", power)
    #print("Top:\t\t", top)
    #print("Bottom:\t\t", bottom)
    #print("Right:\t\t", right)
    #print("Left:\t\t", left)
    #print("\n")



