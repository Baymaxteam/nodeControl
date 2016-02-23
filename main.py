
# import XBee
# import binascii
# from time import sleep
# import platform

# if __name__ == "__main__":

#     if platform.system() == 'Linux':
#         xbee = XBee.XBee("/dev/ttyUSB0")
#     elif platform.system() == 'Darwin':
#         xbee = XBee.XBee("/dev/cu.usbserial-FTYVE8XDA")
#     else:
#         xbee = XBee.XBee("COM9")

    #xbeelisten = XBee.XBee("COM7")
# Windows: xbee = XBee("COM7")
# OSX: xbee = XBee("/dev/cu.usbserial-FTYVE8XDA")
# Ubuntu: xbee = XBee("/dev/ttyUSB0")

    # xbee = XBee.XBee("COM7")  # Your serial port name here
    # A message that requires escaping

    #   L NODE STATE
    #   111 =  6C 07 = 7 100 = 6C 04 =4  001 = 6C 01 = 1
    #   110 =  6C 06 = 6 011 = 6C 03 =3  000 = 6C 00 = 0
    #   101 =  6C 05 = 5 010 = 6C 02 =2
    #   L turn = 6C 08 = 8
    #   M turn = 6C 09 = 9
    #   R turn = 6C 10 = 10

    # Nnode1 = '7E 00 10 10 01 00 13 A2 00 40 EC 3A A4 FF FE 00 00'
    # Nnode2 = '7E 00 10 10 01 00 13 A2 00 40 EC 3A B7 FF FE 00 00'
    # Nnode3 = '7E 00 10 10 01 00 13 A2 00 40 EC 3A 97 FF FE 00 00'
    # Nnode4 = '7E 00 10 10 01 00 13 A2 00 40 B3 2D 41 FF FE 00 00'
    # Nnode5 = '7E 00 10 10 01 00 13 A2 00 40 EC 3A 98 FF FE 00 00'
    # Nnode6 = '7E 00 10 10 01 00 13 A2 00 40 B3 31 65 FF FE 00 00'
    # Lnode1 = '7E 00 10 10 01 00 13 A2 00 40 B3 2D 4F FF FE 00 00'
    # Lnode2 = '7E 00 10 10 01 00 13 A2 00 40 B3 2D 5B FF FE 00 00'

    # Nnode1 = '00 13 A2 00 40 EC 3A A4'
    # Nnode2 = '00 13 A2 00 40 EC 3A B7'
    # Nnode3 = '00 13 A2 00 40 EC 3A 97'
    # Nnode4 = '00 13 A2 00 40 B3 2D 41'
    # Nnode5 = '00 13 A2 00 40 EC 3A 98'
    # Nnode6 = '00 13 A2 00 40 B3 31 65'

    # Lnode1 = '00 13 A2 00 40 B3 2D 4F'
    # Lnode2 = '00 13 A2 00 40 B3 2D 5B'

    # IRnode = '00 13 A2 00 40 EC 3A BE'

              
    

    # rep = xbee.Currentreport()
    # Currentreport = xbeelisten.Receive()
    # rep
    # print(len(Currentreport))
    # print(Currentreport)
    # xbee.node_all_reset()
    # sleep(5)
    # xbee.node_one_reset(IRnode)
    # sleep(5)

    #Node N Open
    # xbee.node_N_all_open()
    # sleep(1.5)
    # xbee.node_N_all_close()

    # sleep(1.5)
    # xbee.node_All_turn(1)
    # sleep(1)
    # xbee.node_All_turn(0)
    # sleep(1)
    # xbee.node_N_one_turn(Nnode1)
    # sleep(1)
    # xbee.node_N_one_turn(1, Nnode5)
    # sleep(1)
    # xbee.node_N_one_turn(0, Nnode5)
    # sleep(1)
    # xbee.node_N_one_turn(Nnode3)
    # sleep(1)
    # xbee.node_N_one_turn(Nnode4)
    # sleep(1)
    # xbee.node_N_one_turn(Nnode5)
    # sleep(1)
    # xbee.node_N_one_turn(Nnode6)
    # sleep(1)
    # xbee.node_L_one_turn(10, Lnode1)
    # sleep(1)
    # xbee.node_L_one_turn(5, Lnode1)
    # sleep(1)
    # xbee.node_L_one_turn(1,Lnode2)
    # sleep(1)
    # xbee.node_L_one_turn(9,Lnode2)
    # sleep(1)
    # xbee.node_L_one_turn(9,Lnode2)
    # sleep(1)
    # xbee.node_N_one_turn(Nnode1)
    # sleep(1)
    # xbee.node_N_one_turn(Nnode2)
    # sleep(1)
    # xbee.node_N_one_turn(Nnode3)
    # sleep(1)
    # xbee.node_N_one_turn(Nnode4)
    # sleep(1)
    # xbee.node_N_one_turn(Nnode5)
    # sleep(1)
    # xbee.node_N_one_turn(Nnode6)
    # sleep(1)
    # xbee.node_L_one_turn(7,Lnode1)
    # sleep(1)
    # xbee.node_L_one_turn(7,Lnode2)
    # sleep(1)

    
    # xbee.IR_node_send("ON")
    # sleep(1)
    # Msg = xbee.Receive()
    # if Msg:
    #     print("Node IR Switch")

    # xbee.IR_node_send(1)
    # sleep(5)
    # Msg = xbee.Receive()
    # if Msg:
    #     print("Node IR Switch")

    # xbee.IR_node_send(2)
    # sleep(1)
    # Msg = xbee.Receive()
    # if Msg:
    #     print("Node IR Switch")

    # xbee.IR_node_send(3)
    # sleep(1)
    # Msg = xbee.Receive()
    # if Msg:
    #     print("Node IR Switch")
    # xbee.Send(bytearray.fromhex("61 00"))
    # sleep(2)
    # Msg = xbee.Receive()
    # if Msg:
    #     print("Node ALL Close")  

    #print (xbee.Currentreport())
    # xbee.IRSend(bytearray.fromhex("72 02 90 04 00 00 0C 00"))
    # sleep(1)
    # Msg = xbee.Receive()
    # if Msg:
    #     print("Node IR Switch")

    # xbee.IRSend(bytearray.fromhex("72 02 90 04 00 00 0C 00"))
    # sleep(1)
    # Msg = xbee.Receive()
    # if Msg:
    #     print("Node IR Switch")        

import XBee
import binascii
from time import sleep
import platform

# if __name__ == "__main__":

    # if platform.system() == 'Linux':
    #     xbee = XBee.XBee("/dev/ttyUSB0")
    # elif platform.system() == 'Darwin':
    #     xbee = XBee.XBee("/dev/cu.usbserial-FTYVE8XDA")
    # else:

xbee = XBee.XBee("COM7")
xbeeListen = XBee.XBee("COM9")
xbeeIRreceive = XBee.XBee("COM8")
# xbee = XBee.XBee("/dev/cu.usbserial-FTYVE8XDC")


# Windows: xbee = XBee("COM7")
# OSX: xbee = XBee("/dev/cu.usbserial-FTYVE8XDA")
# Ubuntu: xbee = XBee("/dev/ttyUSB0")

    # xbee = XBee.XBee("COM7")  # Your serial port name here
    # A message that requires escaping

    #   L NODE STATE
    #   111 =  6C 07 = 7 100 = 6C 04 =4  001 = 6C 01 = 1
    #   110 =  6C 06 = 6 011 = 6C 03 =3  000 = 6C 00 = 0
    #   101 =  6C 05 = 5 010 = 6C 02 =2
    #   L turn = 6C 08 = 8
    #   M turn = 6C 09 = 9
    #   R turn = 6C 10 = 10

    # Nnode1 = '7E 00 10 10 01 00 13 A2 00 40 EC 3A A4 FF FE 00 00'
    # Nnode2 = '7E 00 10 10 01 00 13 A2 00 40 EC 3A B7 FF FE 00 00'
    # Nnode3 = '7E 00 10 10 01 00 13 A2 00 40 EC 3A 97 FF FE 00 00'
    # Nnode4 = '7E 00 10 10 01 00 13 A2 00 40 B3 2D 41 FF FE 00 00'
    # Nnode5 = '7E 00 10 10 01 00 13 A2 00 40 EC 3A 98 FF FE 00 00'
    # Nnode6 = '7E 00 10 10 01 00 13 A2 00 40 B3 31 65 FF FE 00 00'
    # Lnode1 = '7E 00 10 10 01 00 13 A2 00 40 B3 2D 4F FF FE 00 00'
    # Lnode2 = '7E 00 10 10 01 00 13 A2 00 40 B3 2D 5B FF FE 00 00'

Nnode1 = '00 13 A2 00 40 EC 3A A4'
Nnode2 = '00 13 A2 00 40 EC 3A B7'
Nnode3 = '00 13 A2 00 40 EC 3A 97'
Nnode4 = '00 13 A2 00 40 B3 2D 41'
Nnode5 = '00 13 A2 00 40 EC 3A 98'
Nnode6 = '00 13 A2 00 40 B3 31 65'

Lnode1 = '00 13 A2 00 40 B3 2D 4F'
Lnode2 = '00 13 A2 00 40 B3 2D 5B'

IRnode = '00 13 A2 00 40 C2 8B B7'


up1 = '7E 00 52 10 01 00 00 00 00 00 00 00 00 FF FE 00 00 72 00 02 02 92 22 94 11 F4 01 8A 02 90 01 08 07 F4 01 8A 02 90 01 BC 02 C2 01 8A 02 C2 01 BC 02 90 01 BC 02 C2 01 8A 02 C2 01 08 07 C2 01 8A 02 C2 01 08 07 90 01 08 07 C2 01 D6 06 F4 01 D6 06 C2 01 8A 02'
up2 = '7E 00 52 10 01 00 00 00 00 00 00 00 00 FF FE 00 00 72 00 02 01 C2 01 08 07 C2 01 8A 02 C2 01 08 07 C2 01 8A 02 C2 01 8A 02 C2 01 08 07 C2 01 8A 02 C2 01 BC 02 90 01 BC 02 C2 01 D6 06 C2 01 8A 02 F4 01 D6 06 C2 01 08 07 C2 01 8A 02 C2 01 08 07 90 01 08 07'
up3 = '7E 00 1A 10 01 00 00 00 00 00 00 00 00 FF FE 00 00 72 00 02 00 43 00 C2 01 D6 06 C2 01'

    # xbee.node_all_reset()

IRcode = xbeeIRreceive.IRReceive()
# print(IRcode)
pack1 = IRcode[0][0]
pack2 = IRcode[1][0]
pack3 = IRcode[2][0]
print(pack1,pack2,pack3)
xbee.IR_node_send(up1,up2,up3)
# xbee.IR_node_send(pack1,pack2,pack3)

# rep = xbee.CurrentSend()
# sleep(1)
# listen = xbeeListen.Receive()
# print (listen)
# print(len(rep))
# print(rep)

    # xbee.node_one_reset(IRnode)


    #Node N Open
# xbee.node_All_turn(1)
# listen = xbeeListen.Receive()
# print (listen)
# sleep(1.5)
# xbee.node_All_turn(0)
# listen = xbeeListen.Receive()
# print (listen)
    # xbee.node_N_all_close()

    # sleep(1.5)
    # xbee.node_All_turn(1)
    # sleep(1)
    # xbee.node_All_turn(0)
    # sleep(1)
    # xbee.node_N_one_turn(Nnode1)
    # sleep(1)
    # xbee.node_N_one_turn(1, Nnode5)
    # sleep(1)
    # xbee.node_N_one_turn(0, Nnode5)
    # sleep(1)
    # xbee.node_N_one_turn(Nnode3)
    # sleep(1)
    # xbee.node_N_one_turn(Nnode4)
    # sleep(1)
    # xbee.node_N_one_turn(Nnode5)
    # sleep(1)
    # xbee.node_N_one_turn(Nnode6)
    # sleep(1)
    # xbee.node_L_one_turn(10, Lnode1)
    # sleep(1)
    # xbee.node_L_one_turn(5, Lnode1)
    # sleep(1)
    # xbee.node_L_one_turn(1,Lnode2)
    # sleep(1)
    # xbee.node_L_one_turn(9,Lnode2)
    # sleep(1)
    # xbee.node_L_one_turn(9,Lnode2)
    # sleep(1)
    # xbee.node_N_one_turn(Nnode1)
    # sleep(1)
    # xbee.node_N_one_turn(Nnode2)
    # sleep(1)
    # xbee.node_N_one_turn(Nnode3)
    # sleep(1)
    # xbee.node_N_one_turn(Nnode4)
    # sleep(1)
    # xbee.node_N_one_turn(Nnode5)
    # sleep(1)
    # xbee.node_N_one_turn(Nnode6)
    # sleep(1)
    # xbee.node_L_one_turn(7,Lnode1)
    # sleep(1)
    # xbee.node_L_one_turn(7,Lnode2)
    # sleep(1)

    
# xbee.IR_node_send("DOWN")
    # sleep(1)
    # Msg = xbee.Receive()
    # if Msg:
    #     print("Node IR Switch")

    # xbee.IR_node_send(1)
    # sleep(5)
    # Msg = xbee.Receive()
    # if Msg:
    #     print("Node IR Switch")

    # xbee.IR_node_send(2)
    # sleep(1)
    # Msg = xbee.Receive()
    # if Msg:
    #     print("Node IR Switch")

    # xbee.IR_node_send(3)
    # sleep(1)
    # Msg = xbee.Receive()
    # if Msg:
    #     print("Node IR Switch")
    # xbee.Send(bytearray.fromhex("61 00"))
    # sleep(2)
    # Msg = xbee.Receive()
    # if Msg:
    #     print("Node ALL Close")  

    #print (xbee.Currentreport())
    # xbee.IRSend(bytearray.fromhex("72 02 90 04 00 00 0C 00"))
    # sleep(1)
    # Msg = xbee.Receive()
    # if Msg:
    #     print("Node IR Switch")

    # xbee.IRSend(bytearray.fromhex("72 02 90 04 00 00 0C 00"))
    # sleep(1)
    # Msg = xbee.Receive()
    # if Msg:
    #     print("Node IR Switch")        