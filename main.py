
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


# xbee = XBee.XBee("COM7")
# xbeeListen = XBee.XBee("COM9")
# xbeeIRreceive = XBee.XBee("COM8")

xbee = XBee.XBee("/dev/cu.usbserial-FTYVE8XDA")
xbeeIRreceive = XBee.XBee("/dev/cu.usbserial-FTYVE8XDB")
xbeeListen = XBee.XBee("/dev/cu.usbserial-FTYVE8XDC")

# Windows: xbee = XBee("COM7")
# OSX: xbee = XBee("/dev/cu.usbserial-FTYVE8XDA")
# Ubuntu: xbee = XBee("/dev/ttyUSB0")


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





IRnode = '00 13 A2 00 40 EC 3A BE'

### ------------------ ###
### ---電流封包測試--- ###
### ------------------ ###

# xbee.CurrentSend()
# sleep(1)
# listen = xbeeListen.Receive()
# print (listen)

### -------------------- ###
### ---紅外線對碼測試--- ###
### -------------------- ###

IRcode = []
IRcode = xbeeIRreceive.IRReceive()
print(IRcode)
pack1 = IRcode[0]

IRcode = []
IRcode = xbeeIRreceive.IRReceive()
print(IRcode)
pack1 = IRcode[0]
# xbee.IR_compare_send(pack1)

### -------------------- ###
### ---紅外線內建測試--- ###
### -------------------- ###

# xbee.IR_node_send("power")
# xbee.IR_node_send("chup")
# xbee.IR_node_send("chdown")
# xbee.IR_node_send("voiceup")
# xbee.IR_node_send("voicedown")
# xbee.IR_node_send("mute")
# xbee.IR_node_send("back")
# xbee.IR_node_send("tv1")
# xbee.IR_node_send("tv4")
# xbee.IR_node_send("enter")
# xbee.IR_node_send("language")
# xbee.IR_node_send("display")
# xbee.IR_node_send("scan")
# xbee.IR_node_send("info")
# xbee.IR_node_send("energy")
# xbee.IR_node_send("boardcast")

### ---------------------- ###
### ---節點重設(無回應)--- ###
### ---------------------- ###

# xbee.node_all_reset()
# xbee.node_one_reset(Nnode2)

### --------------------- ###
### ---節點N開啟or關閉--- ###
### --------------------- ###

# xbee.node_N_one_turn(1, Nnode4)
# sleep(1)
# xbee.node_N_one_turn(0, Nnode4)

### --------------------- ###
### ---節點L開啟or關閉--- ###
### --------------------- ###
# xbee.node_L_one_turn(8,Lnode1)
# sleep(2)
# xbee.node_L_one_turn(9,Lnode1)
# sleep(2)
# xbee.node_L_one_turn(10,Lnode1)
# sleep(2)
# xbee.node_L_one_turn(7,Lnode1)
# listen = xbeeListen.Receive()
# print (listen)
# xbee.node_L_one_turn(7,Lnode2)

### ------------------------ ###
### ---節點全部開啟or關閉--- ###
### ------------------------ ###
# xbee.node_All_turn(1)
# xbee.node_All_turn(0)

### ------------------- ###
### ---節點N循環測試--- ###
### ------------------- ###
# X=0.5
# i=0
# while(i<5):
    # xbee.node_N_one_turn(1, Nnode1)
    # sleep(X)
    # xbee.node_N_one_turn(0, Nnode1)
    # sleep(X)
    # xbee.node_N_one_turn(1, Nnode2)
    # sleep(X)
    # xbee.node_N_one_turn(0, Nnode2)
    # # # sleep(X)
    # xbee.node_N_one_turn(1, Nnode3)
    # sleep(X)
    # xbee.node_N_one_turn(0, Nnode3)
    # sleep(X)
    # xbee.node_N_one_turn(1, Nnode4)
    # sleep(X)
    # xbee.node_N_one_turn(0, Nnode4)
    # sleep(X)
    # xbee.node_N_one_turn(1, Nnode5)
    # sleep(X)
    # xbee.node_N_one_turn(0, Nnode5)
    # sleep(X)
    # xbee.node_N_one_turn(1, Nnode6)
    # sleep(X)
    # xbee.node_N_one_turn(0, Nnode6)
    # sleep(X)
    # i=i+1


    
