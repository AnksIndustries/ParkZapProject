#           this is a program to fetch student-ID data from server and save
#           the JSON data in the persistent memory. Once the data is saved
#           then using the serial console if anybody types a valid student-ID
#           light up an LED on any of the IO posts.

#           Author: - Ankit Aditya
#           Created On: - 10/6/2019

########### Client Side program ##############################################

import socket

RUN = True
ip = "<Enter Your microcontroller's Ip here>"          # microcontroller's ip address
port = 5050                                            # port number should be same as microcontroller's port address
buffer_size = 1024                                     # buffer size to receive message


client_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM) # client side TCP_IP socket creation for serial communication

try:                                            # try to connect to the microcontroller
    client_socket.connect((ip,port))
    print('successfully connected to server ', ip,' and port ',port)
except socket.error as e:
    print('problem in connecting to server: ',e)

studentID = input('Enter the Id to match or exit to close!')     # input from user of student Id

while(RUN):                                                      # run the program till user exits the program
    client_socket.send(studentID.encode('utf-8'))
    dataRecieve = client_socket.recv(buffer_size)
    dataRecieve = dataRecieve.decode('utf-8')
    print(dataRecieve)                                           # print the data recieved
    studentID = input('Enter the Id to match or exit to close!')

    if studentID.upper()=='EXIT':
        RUN = False
        break
