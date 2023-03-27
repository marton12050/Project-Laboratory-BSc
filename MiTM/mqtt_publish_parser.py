from Mqtt_Parser import Mqtt_Parser

class Mqtt_Publish_Parser(Mqtt_Parser):
    def __init__(self,mqtt):
        self.packet = mqtt
        self.messageType = mqtt[0]
        self.messageTypeCode,self.messageTypeWord = self.typeMap(mqtt[0])
        self.messageLength = mqtt[1]
        self.messageLengthNum = self.messageLength
        self.topicLength = mqtt[2:4]
        self.topicLengthNum = int.from_bytes(self.topicLength,"big")
        self.topicName = mqtt[4:self.topicLengthNum+4]
        self.message = mqtt[self.topicLengthNum+4:][:self.messageLengthNum]

    
    def changeTopic(self,newTopic):
        topic = []
        for letter in newTopic:
            topic.append(ord(letter))
        self.topicName = topic
        self.topicLengthNum = len(newTopic)
        self.topicLength = self.topicLengthNum.to_bytes(2,"big")

    def changeMessage(self,newMessage):
        self.messageWords = newMessage
        self.messageLengthNum = self.topicLengthNum + 2 + len(newMessage)
        self.messageLength = self.messageLengthNum
        message = []
        for letter in newMessage:
            message.append(ord(letter))
        self.message = message

    def getHex(self):
        full = []
        full.append(self.messageType)
        full.append(self.messageLength)
        [full.append(x) for x in self.topicLength]
        [full.append(x) for x in self.topicName]
        [full.append(x) for x in self.message]
        return(full)


if __name__=="__main__":#Tesztelés
    asd = Mqtt_Publish_Parser(b'0\x1f\x00\x0bTemperature6. tempeture: 50.0')
    print(b'0\x1f\x00\x0bTemperature6. tempeture: 50.0')
    print(len(asd.getHex()))
    print(bytes(asd.getHex()))
    asd.changeTopic("Temperatur")
    asd.changeMessage("6. tempeture: 50.0")
    print(bytes(asd.getHex()))
    print(len(asd.getHex()))