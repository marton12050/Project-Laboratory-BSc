#!/usr/bin/python3

import socket
import select
import threading
import queue

from config_check import Config_Check
from Mqtt_Parser import Mqtt_Parser
from interactive import interactive

SOCKET_HOST = 'localhost'
SOCKET_PORT = 9998

MQTT_HOST = "localhost"
MQTT_PORT = 1883


class MiTM:
    """
    Simply forwarding yet
    """
    def __init__(self, myip,myport, dip, dport):
        self.IP = myip
        self.PORT = myport
        self.BROKER_IP = dip
        self.BROKER_PORT = dport
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.rules = Config_Check()
        
    def listen(self, num=1):
        """
        Server side starts listening on given address
        """
        self.server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.server.bind((SOCKET_HOST, SOCKET_PORT))

        print("The server side starts listening.")
        
        self.server.listen(num)
        client, addr = self.server.accept()
        self.server.close()

        self.forwarding(client, addr)
    
    def forwarding(self, client : socket, rtnaddr):
        forwarder = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        forwarder.connect((self.BROKER_IP, self.BROKER_PORT))

        connected = True
        
        interactive_tasks = queue.Queue(-1)
        threading.Thread(target=interactive, args=(interactive_tasks,), daemon=True).start()

        while connected:
            
            rsocket = select.select([client, forwarder], [], [])[0]

            if client in rsocket:
                buffer = client.recv(2048)
                if len(buffer) == 0:
                    connected = False
                    break
                # here change the data to the broker
                mqttpacket = Mqtt_Parser(buffer)      #Parse the MQTT packet
                respond = self.rules.check(mqttpacket)#Check the rules from the config and logging

                if respond == True:
                    #print("Data forwarding to broker:",buffer)
                    forwarder.sendall(buffer)
                elif respond == False:
                    pass
                elif respond == None:
                    interactive_tasks.put((forwarder,mqttpacket))
                else:
                    buffer = respond.getHex()
                    #print("Data forwarding to broker:",buffer)
                    forwarder.sendall(buffer)

            if forwarder in rsocket and connected:
                buffer = forwarder.recv(2048)
                if len(buffer) == 0:
                    connected = False
                    break
                # here change the data to the client
                mqttpacket = Mqtt_Parser(buffer) 
                respond = self.rules.check(mqttpacket)
                
                if respond == True:
                    #print("Data forwarding to client:",buffer)
                    client.sendall(buffer)
                elif respond == False:
                    pass
                elif respond == None:
                    interactive_tasks.put((client,mqttpacket))
                else:
                    buffer = respond.getHex()
                    #print("Data forwarding to client:",buffer)
                    client.sendall(buffer)
            

        try:
            client.close()
        except:
            pass

        try:
            forwarder.close()
        except:
            pass

if __name__ == '__main__':
    mitm = MiTM(SOCKET_HOST, SOCKET_PORT, MQTT_HOST, MQTT_PORT)
    mitm.listen()