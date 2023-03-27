


class Mqtt_Parser:
    def __init__(self,mqtt):   
        self.packet = mqtt
        self.messageType = mqtt[0]
        self.messageTypeCode,self.messageTypeWord = self.typeMap(mqtt[0])
        self.messageLength = mqtt[1]
        self.messageLengthNum = self.messageLength
        if self.messageTypeCode == 1:
            self.connectflag = mqtt[9]
            #if hasauth():
            self.ClientIDLength = mqtt[12:14]
            self.ClientIDLengthNum = int.from_bytes(self.ClientIDLength,"big")
            self.ClientID = mqtt[14:self.ClientIDLengthNum+14]
            self.UserNameLength = mqtt[self.ClientIDLengthNum+14:self.ClientIDLengthNum+14+2]
            self.UserNameLengthNum = int.from_bytes(self.UserNameLength,"big")
            self.UserName = mqtt[self.ClientIDLengthNum+16:self.ClientIDLengthNum+16+self.UserNameLengthNum]
            self.PasswordLength = mqtt[self.ClientIDLengthNum+16+self.UserNameLengthNum:self.ClientIDLengthNum+16+self.UserNameLengthNum+2]
            self.PasswordLengthNum = int.from_bytes(mqtt[self.ClientIDLengthNum+16+self.UserNameLengthNum:self.ClientIDLengthNum+16+self.UserNameLengthNum+2],"big")
            self.Password = mqtt[self.ClientIDLengthNum+18+self.UserNameLengthNum:self.ClientIDLengthNum+16+self.UserNameLengthNum+4+self.PasswordLengthNum]
        elif self.messageTypeCode == 3:
            self.topicLength = mqtt[2:4]
            self.topicLengthNum = int.from_bytes(self.topicLength,"big")
            self.topicName = mqtt[4:self.topicLengthNum+4]
            self.message = mqtt[self.topicLengthNum+4:][:self.messageLengthNum]


    def typeMap(self,hexVal):
        ControlType = hexVal>>4
        hexToControlType = {
        0:"Reserved",1:"Connection request",2:"Connect acknowledgment",3:"Publish message",4:"Publish acknowledgment (QoS 1)",5:"Publish received (QoS 2 delivery part 1)",
        6:"Publish release (QoS 2 delivery part 2)",7:"Publish complete (QoS 2 delivery part 3)",8:"Subscribe request",9:"Subscribe acknowledgment",10:"Unsubscribe request",
        11:"Unsubscribe acknowledgmen",12:"PING request",13:"PING response",14:"Disconnect notification",15:"Authentication exchange"
        }
        b = hexToControlType[ControlType]
        return ControlType,b

    def changeTopic(self,newTopic):
        topic = []
        self.messageLengthNum = len(newTopic) - self.topicLengthNum + self.messageLengthNum
        self.messageLength = self.messageLengthNum
        for letter in newTopic:
            topic.append(ord(letter))
        self.topicName = bytes(topic)
        self.topicLengthNum = len(newTopic)
        self.topicLength = self.topicLengthNum.to_bytes(2,"big")

    def changeMessage(self,newMessage):
        self.messageWords = newMessage
        self.messageLengthNum = self.topicLengthNum + 2 + len(newMessage)
        self.messageLength = self.messageLengthNum
        message = []
        for letter in newMessage:
            message.append(ord(letter))
        self.message = bytes(message)

    def getHex(self):
        if self.messageTypeCode == 3:
            full = []
            full.append(self.messageType)
            full.append(self.messageLength)
            [full.append(x) for x in self.topicLength]
            [full.append(x) for x in self.topicName]
            [full.append(x) for x in self.message]
            return bytes(full)
        else:
            return self.packet
