import XBee
import binascii
from time import sleep

if __name__ == "__main__":
    xbee = XBee.XBee("COM7")  # Your serial port name here
    # A message that requires escaping

    print (xbee.Currentreport())

    #Node N Open


    xbee.node_N_all_open()
    sleep(1)
    xbee.node_N_all_close()
    sleep(1)
    xbee.node_All_open()
    sleep(1)
    xbee.node_All_close()
    sleep(1)
    xbee.node_N_one_open('7E 00 10 10 01 00 13 A2 00 40 EC 3A B7 49 68 00 00')
    sleep(1)
    xbee.node_N_one_close('7E 00 10 10 01 00 13 A2 00 40 EC 3A B7 49 68 00 00')
    sleep(1)

    # xbee.Send(bytearray.fromhex("6C 01"))
    # sleep(2)
    # Msg = xbee.Receive()
    # if Msg:
    #     print("Node L 1 open")


    # xbee.Send(bytearray.fromhex("6C 02"))
    # sleep(2)
    # Msg = xbee.Receive()
    # if Msg:
    #     print("Node L 2 open")

    # xbee.Send(bytearray.fromhex("6C 03"))
    # sleep(2)
    # Msg = xbee.Receive()
    # if Msg:
    #     print("Node L 1 2 open")

    # xbee.Send(bytearray.fromhex("6C 04"))
    # sleep(2)
    # Msg = xbee.Receive()
    # if Msg:
    #     print("Node L 3 open")

    # xbee.Send(bytearray.fromhex("6C 07"))
    # sleep(2)
    # Msg = xbee.Receive()
    # if Msg:
    #     print("Node L ALL open")

    # xbee.Send(bytearray.fromhex("61 00"))
    # sleep(2)
    # Msg = xbee.Receive()
    # if Msg:
    #     print("Node ALL Close")  

    # xbee.IRSend(bytearray.fromhex("72 02 90 04 00 00 0C 00"))
    # sleep(3)
    # Msg = xbee.Receive()
    # if Msg:
    #     print("Node IR Switch")

    # xbee.IRSend(bytearray.fromhex("72 02 90 04 00 00 0C 00"))
    # sleep(3)
    # Msg = xbee.Receive()
    # if Msg:
    #     print("Node IR Switch")        
