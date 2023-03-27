from datetime import datetime
import re

import util
from Mqtt_Parser import Mqtt_Parser

class Config_Check():
    def __init__(self, filename="config.conf"):
        self.configfile = filename
        self.dumpfile = None
        self.topicfile = None 
        self.authfile = None
        self.knowntopics = None

        self.rulesTopic = []
        self.rulesMsg = []

        self.default = True
        self.read_config()


    def read_config(self):
        config = open(self.configfile, "r")
        numline = 0
        for line in config:
            numline += 1
            line = line.strip()
            if len(line) == 0 or line[0] == '#':
                continue
            command = line.split()
            try:
                if command[0] == "SAVE":
                    self.save(command[1:])
                elif command[0] == "ALLOW":
                    self.allow(command[1:])
                elif command[0] == "DISALLOW":
                    self.disallow(command[1:]) 
                elif command[0] == "CHANGE":
                    self.change(command[1:])
                elif command[0] == "INTERACTIVE":
                    self.interactive(command[1:])
            except SyntaxError as e:
                print("Syntax error on line {} in config".format(numline))

        config.close()

    def save(self, command):
        if len(command) == 1:
            filename = command[0].strip('"')
            self.dumpfile = filename
        elif len(command) == 2:
            if command[0] == "topic":
                filename = command[1].strip('"')
                self.topicfile = filename
                with open(self.topicfile, "r") as f:
                    self.knowntopics = f.read().splitlines()

            if command[0] == "auth":
                filename = command[1].strip('"')
                self.authfile = filename
        else:
            raise SyntaxError

    def allow(self, command):
        if len(command) >= 2:
            util.valid_regex(command[1].strip('"'))

        def isallow(msg):
            if re.search(command[1].strip('"'),msg) == None:
                return None
            return True

        rule = isallow
        if command[0] == "TOPIC":
            self.rulesTopic.append(rule)
        elif command[0] == "MSG":
            self.rulesMsg.append(rule)
        elif command[0] == "DEFAULT":
            self.default = True
        else:
            raise SyntaxError

    def disallow(self,command):
        if len(command) >= 2:
            util.valid_regex(command[1].strip('"'))
            
        def isallow(msg):
            if re.search(command[1].strip('"'),msg) == None:
                return None
            return False
        rule = isallow
        if command[0] == "TOPIC":
            self.rulesTopic.append(rule)
        elif command[0] == "MSG":
            self.rulesMsg.append(rule)
        elif command[0] == "DEFAULT":
            self.default = False
        else:
            raise SyntaxError

    def change(self, command):
        if len(command) >= 2:
            util.valid_regex(command[2].strip('"'))

        def isallow(msg):
            if re.search(command[2].strip('"'),msg) == None:
                return None
            return command[4].strip('"')

        if command[0] == "TOPIC":
            if command[1] == "if":
                frommsg = command[2].strip('"')
                if command[3] == "to":
                    self.rulesTopic.append(isallow)
                    return
        elif command[0] == "MSG":
            if command[1] == "if":
                frommsg = command[2].strip('"')
                if command[3] == "to":
                    self.rulesMsg.append(isallow)
                    return
                
        raise SyntaxError

    def interactive(self, command):
        if len(command) >= 2:
            util.valid_regex(command[1].strip('"'))

        def isallow(msg):
            if re.search(command[1].strip('"'),msg) == None:
                return None
            return 2

        rule = isallow
        if command[0] == "TOPIC":
            self.rulesTopic.append(rule)
        elif command[0] == "MSG":
            self.rulesMsg.append(rule)
        else:
            raise SyntaxError

            

    def check(self, packet: Mqtt_Parser):
        ##  Write logs    ##
        if self.dumpfile != None:
            with open(self.dumpfile, "a") as f:
                f.write(str(datetime.now())+":"+str(packet.getHex())+"\n")

        if packet.messageTypeCode != 3:
            if packet.messageTypeCode == 1:
                if self.authfile != None:
                    with open(self.authfile, "a+") as f:
                        f.write(str(datetime.now())+":"+packet.ClientID.decode()+":"+packet.UserName.decode()+":"+packet.Password.decode()+"\n")
            return True
        if packet.messageTypeCode != 3:
            return True
        if self.topicfile != None and packet.topicName.decode() not in self.knowntopics: 
            #print(self.knowntopics)
            self.knowntopics.append(packet.topicName.decode())
            with open(self.topicfile, "a+") as f:
                        f.write(packet.topicName.decode()+"\n")

        ## Check filters ##
        ri = 0
        for rule in self.rulesTopic:
            ri +=1
            respond = rule(packet.topicName.decode())
            if respond == None:
                continue
            elif respond == True:
                break
            elif respond == False:
                #print("topic rule applied",ri)
                return False
            elif respond == 2:
                #print("topic interactive rule applied",ri)
                return None
            elif type(respond) is str:
                packet.changeTopic(respond)
                break
            else:
                raise "Invalid respond from rules"
        ri = 0
        for rule in self.rulesMsg:
            ri += 1
            respond = rule(packet.message.decode())
            #print("respond",respond)
            if respond == None:
                continue
            elif respond == True:
                #print("msg rule applied",ri)
                return packet
            elif respond == False:
                #print("msg rule applied",ri)
                return False
            elif respond == 2:
                #print("interactive rule")
                return None
            elif type(respond) is str:
                #print("msg rule applied",ri)
                packet.changeMessage(respond)
                return packet
            else:
                raise "Invalid respond from rules"
        
        if self.default:
            return packet
        else:
            return False
            