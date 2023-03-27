from Mqtt_Parser import Mqtt_Parser

import queue

def interactive(packets:queue.Queue):

    while True:
        target, packet = packets.get()
        task_done = False
        while not task_done:
            print("What to do with this packet?")
            print_packet_with_style(packet)

            print("1. Allow")
            print("2. Disallow")
            print("3. Change")

            data = input("")

            if data == "1":
                print(packet.getHex())
                target.sendall(packet.getHex())
                task_done = True
            elif data == "2":
                task_done = True
            elif data == "3":
                while True:
                    print_packet_with_style(packet)
                    print("1. Change topic")
                    print("2. Change message")
                    print("3. Send changed message")
                    print("4. Exit")
                    data = input("")
                    if data == "1":
                        data = input("Change topic '{}' to \n".format(packet.topicName.decode()))
                        packet.changeTopic(data)
                    elif data == "2":
                        data = input("Change message '{}' to \n".format(packet.message.decode()))
                        packet.changeMessage(data)
                    elif data == "3":
                        packets.task_done()
                        print(packet.getHex())
                        target.sendall(packet.getHex())
                        task_done = True
                        break
                    elif data == "4":
                        break
                    else:
                        print("invalid")

            else:
                print("invalid")
        packets.task_done()


def print_packet_with_style(packet: Mqtt_Parser):
    print("MQTT packet " + packet.messageTypeWord)
    print("      - Topic: '" + packet.topicName.decode() + "'")
    print("      - Message: '" + packet.message.decode() + "'")


if __name__=="__main__":
    a = Mqtt_Parser(b'0\x1f\x00\x0bTemperature6. tempeture: 50.0')
