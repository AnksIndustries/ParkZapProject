#           this is a program to fetch student-ID data from server and save
#           the JSON data in the persistent memory. Once the data is saved
#           then using the serial console if anybody types a valid student-ID
#           light up an LED on any of the IO posts.

#           Author: - Ankit Aditya
#           Created On: - 10/6/2019
 
# class to fetch and process student data and display on serial output screen
import requests, json, urllib  # modules for get request, reading json file and
                               # for opening url respectively

import socket                  # for starting the server and setting up the socket
import sys                     # for handling system console
import os.path                 # file exists or not

import RPi.GPIO as GPIO        # to use GPIO pins of raspberry pi
import time                    # to set the led to blink for 5 seconds
GPIO.setmode(GPIO.BCM)
GPIO.setup(4,GPIO.OUT)         # set pin 4 for output

def LEDGLOW():                 # Glow the LED for five seconds on pin 4
    GPIO.output(4,GPIO.HIGH)
    time.sleep(5)
    GPIO.output(4,GPIO.LOW)


################# Definition of Global Variables ##################################


Found_Flag = False                                              # true if found the student id
server_url = 'http://demo2378447.mockable.io/student_data';     # url to fetch data                          
server_ip = "<Type the server's ip address>"                    # server ip address
server_port = 5050                                              # server port address can be changed
no_of_clients = 5                                               # number of clients to connect to the server

class studentRecord:            # class for fetching, saving, displaying and 
                                # processing student Record
    def __init__(self,url):
        print("System starting...")
        self.url = url
        try:                    #try for connection to server for Student Records
            getData = requests.get(self.url)
            self.studentData = getData.json()
            with open('StudentRec.json','a+') as file:              # saving the record to the file named 'StudentRec.json'
                json.dump(self.studentData,file)                
        except requests.exceptions.Timeout:                         # exception if url server timeout 
            print('Server timeout for ',self.url)
        except requests.exceptions.TooManyRedirects:                # exception if too many redirects
            print('Too many redirects on link: ',self.url)
        except requests.exceptions.RequestException as e:           # exception if get request fails
            print(e)
            sys.exit(1)

    def __init__(self):
        print("System starting...")                                 # method overloading of __init__ method if file already exists this method is called

    def searchID(self,ids):                                         # returns true if ID exists else returns false
        with open('StudentRec.json','r') as recordsFile:
            studentRec = json.load(recordsFile)
            for studentID in studentRec['student_id']:
                for sno in studentID:
                    if ids in studentID[sno]:
                        print(studentID[sno],' Found!')
                        Found_Flag=True
                        return True

            if Found_Flag==False:
                print(ids,' not found!!')
                return False


if(os.path.exists('StudentRec.json')):                              # if file doesn't exist it saves the file from the server else use the existing file
    stRc = studentRecord()
else:
    stRc = studentRecord(server_url)


################################################################################
############################# Serial Console program ###########################
################################################################################

class serialIOconsoleServer:                                                            
    def __init__(self,ip,port,numberOfClients):                                     # starts the server with (microcontroller's ip, port no., number of clients)
        self.ip = ip
        self.port = port
        self.numOfClients = numberOfClients
        self.ServerSocket = None                                                    
        try:
            self.ServerSocket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)    # socket creation with TCP_IP protocol
            print('Server Socket Successfully created.')
        except socket.error as e:
            print('socket creation failed with error: ',e)

        try:
            print('binding...')                                                     # binding ip and port 
            ainfo = socket.getaddrinfo(self.ip,self.port)

            self.ServerSocket.bind(ainfo[0][4])
        except socket.error as e:
            print('failed to bind: ',e)
            sys.exit(1)


    def listenToClients(self):                                                      # listens to clients request for searching id and replys
        self.ServerSocket.listen(self.numOfClients)
        print('Listening to ',self.numOfClients,' clients')
        while True:
            conn , addr = self.ServerSocket.accept()
            data = conn.recv(1000)

            if not data:
                continue
            else:
                print('got request! \n sending reply!')
                messages = sendReply(data)
                conn.sendall(messages.encode('utf-8'))
                conn.close()
    
    def closeServer(self):                                                          # Socket is closed
        print('closing server!')
        self.ServerSocket.close()
        sys.exit(1)


def sendReply(data):                                                                # decode and encode message for sending reply and matching the recieved data
    requestedIdToMatch = data.decode('utf-8')
    requestedIdToMatch = requestedIdToMatch.strip()
    if(stRc.searchID(requestedIdToMatch)):
        LEDGLOW()
        Found_Flag=False
        return 'found! \n Led ON for 5 seconds!'
    

if __name__ == '__main__':
    SerialComm =  serialIOconsoleServer(server_ip,server_port,no_of_clients)
    SerialComm.listenToClients()
    SerialComm.closeServer()
