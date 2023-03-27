from Mqtt_Parser import Mqtt_Parser

class Mqtt_Connect_Parser(Mqtt_Parser):
    
    def __init__(self,mqtt):   
        self.packet = mqtt
        self.messageType = mqtt[0]
        self.messageTypeCode,self.messageTypeWord = self.typeMap(mqtt[0])
        self.messageLength = mqtt[1]
        self.messageLengthNum = self.messageLength
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

    def getHex(self):
        return self.packet


if __name__=="__main__":#Tesztelés
    temp = Mqtt_Connect_Parser(b'\x10(\x00\x04MQTT\x04\xc2\x00<\x00\x08mqttpub1\x00\x04User\x00\x0cKecskesajt19')
    print(b'\x10(\x00\x04MQTT\x04\xc2\x00<\x00\x08mqttpub1\x00\x04User\x00\x0cKecskesajt19')
    print(len(temp.getHex()))
    print(bytes(temp.getHex()))
    print(temp.Password,temp.UserName)