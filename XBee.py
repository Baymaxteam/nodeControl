
import serial
from collections import deque
from time import sleep


class XBee():
    RxBuff = bytearray()
    RxMessages = deque()
    nodeCurrent = []
    # node_address ={'00 13 A2 00 40 EC 3A A4':'Nnode1', '00 13 A2 00 40 EC 3A B7':'Nnode2', 
    #                '00 13 A2 00 40 EC 3A 97':'Nnode3', '00 13 A2 00 40 B3 2D 41':'Nnode4',
    #                '00 13 A2 00 40 EC 3A 98':'Nnode5', '00 13 A2 00 40 B3 31 65':'Nnode6',
    #                '00 13 A2 00 40 B3 2D 4F':'Lnode1', '00 13 A2 00 40 B3 2D 5B':'Lnode2',
    #                '00 13 A2 00 40 C2 8B B7':'IRnode'}
                   
    def __init__(self, serialport, baudrate=9600):
        self.serial = serial.Serial(port=serialport, baudrate=baudrate)
        # self.serialRE = serial.Serial(port='COM9', baudrate=baudrate)
    def Receive(self):
        """
           Receives data from serial and checks buffer for potential messages.
           Returns the next message in the queue if available.
        """
        self.nodeCurrent = [] # 清空
        self.nodeState = []
        self.RxMessages.clear()
        remaining = self.serial.inWaiting()
        while remaining:
            chunk = self.serial.read(remaining)
            remaining -= len(chunk)
            self.RxBuff.extend(chunk)

        msgs = self.RxBuff.split(bytes(b'\x7E'))

        #### DEBUG用 
        # a = list(self.RxBuff)
        # t = ((""+' '.join(['%02.x']*len(a))+"") % tuple(a)).upper()
        # print("DEBUG: "+t)
        ####

        for msg in msgs[:-1]:
            # print("msg: ")
            # print(msg)
            if(len(msg)>0): # 避免空的訊息
                self.Validate(msg)


        self.RxBuff = (bytearray() if self.Validate(msgs[-1]) else msgs[-1])

        if self.RxMessages: # 如果 self.RxMessages 有東西
            for msg in self.RxMessages :

                #### DEBUG
                decodePAK = list(msg)
                # print(decodePAK)
                # t = ((""+' '.join(['%02.x']*len(decodePAK))+"") % tuple(decodePAK)).upper()
                # print("DEBUG: "+t)
                ####

                ## 用封包長度確認收到的封包種類
                decodePAK = list(msg)
                packageLen = decodePAK[1]
                ##
                # node 全開、全關
                # n 全開、全關
                # p 封包
                if(packageLen == 13): # P package
                    print('收到P封包')
                if(packageLen == 17):
                    print("收到電流封包") 
                    result = self.Currentreport(msg)
                    # print(result)
                    self.nodeCurrent.append(result)
                if(packageLen == 14):
                    print('收到狀態封包')
                    result = self.Statereport(msg)
                    # print(result)
                    self.nodeCurrent.append(result)
                if(packageLen == 16):
                    print('收到對碼封包')
                # else:
                #     print('無法辨認')
            return self.nodeCurrent
           #return self.RxMessages.popleft()
        else:
            return None

    def IRReceive(self):
        """
           Receives data from serial and checks buffer for potential messages.
           Returns the next message in the queue if available.
        """
        print('請於一秒後按下')
        sleep(3)
        self.RxMessages.clear()
        remaining = self.serial.inWaiting()
        IRPack = []
        while remaining:
            chunk = self.serial.read(remaining)
            remaining -= len(chunk)
            self.RxBuff.extend(chunk)

        msgs = self.RxBuff.split(bytes(b'\x7E'))

        #### DEBUG用 
        # a = list(self.RxBuff)
        # t = ((""+' '.join(['%02.x']*len(a))+"") % tuple(a)).upper()
        # print("DEBUG: "+t)
        ####

        for msg in msgs[:-1]:
            # print("msg: ")
            # print(msg)
            if(len(msg)>0): # 避免空的訊息
                self.Validate(msg)


        self.RxBuff = (bytearray() if self.Validate(msgs[-1]) else msgs[-1])
        if self.RxMessages: # 如果 self.RxMessages 有東西
            for msg in self.RxMessages :
                #### DEBUG
                decodePAK = msg
                # print(decodePAK)
                t = ((""+' '.join(['%02.x']*len(decodePAK))+"") % tuple(decodePAK)).upper()
                # print("DEBUG: "+t)
                ####

                IRPack.append("7E "+t[:-3])
                # print ("IRPACK"+str(IRPack))
                ## 用封包長度確認收到的封包種類
                decodePAK = list(msg)
                packageLen = decodePAK[1]
                ##
                # node 全開、全關
                # n 全開、全關
                # p 封包
                if(packageLen == 22): # IR package
                    print('收到IR封包')
                else:
                    print('無法辨認，請重新對碼')
            return IRPack
           #return self.RxMessages.popleft()
        else:
            print('無收到紅外線，請重新對碼')
            return None

    def Validate(self, msg):
        """
        Parses a byte or bytearray object to verify the contents are a
          properly formatted XBee message.

        Inputs: An incoming XBee message

        Outputs: True or False, indicating message validity
        """


        # print('msg:{0}'.format(msg))

        # 9 bytes is Minimum length to be a valid Rx frame
        #  LSB, MSB, Type, Source Address(2), RSSI,
        #  Options, 1 byte data, checksum
        if (len(msg) - msg.count(bytes(b'0x7D'))) < 9:
            return False
        # if
       # print('msg:{0}'.format(msg))

        # All bytes in message must be unescaped before validating content
        # frame = self.Unescape(msg)

        frame = msg
        #print(frame)
        # print('frame:{0}'.format(frame))
        if(frame == None or len(frame)==0):
            return False

        LSB = frame[1]

        
        if(msg == None or len(msg)==0):
            return False
        LSB = msg[1]
        # Frame (minus checksum) must contain at least length equal to LSB
        if LSB > (len(msg[2:]) - 1):
            return False

        # Validate checksum
        if (sum(msg[2:3+LSB]) & 0xFF) != 0xFF:
            return False

        self.RxMessages.append(msg)
        return True


    def SendStr(self, msg, addr=0xFFFF, options=0x01, frameid=0x00):
        """
        Inputs:
          msg: A message, in string format, to be sent
          addr: The 16 bit address of the destination XBee
            (default: 0xFFFF broadcast)
          options: Optional byte to specify transmission options
            (default 0x01: disable acknowledge)
          frameid: Optional frameid, only used if Tx status is desired
        Returns:
          Number of bytes sent
        """
        return self.Send(msg.encode('utf-8'), addr, options, frameid)


    def Send(self, msg, addr=0xFFFF, options=0x01, frameid=0x00):
        """
        Inputs:
          msg: A message, in bytes or bytearray format, to be sent to an XBee
          addr: The 16 bit address of the destination XBee
            (default broadcast)
          options: Optional byte to specify transmission options
            (default 0x01: disable ACK)
          frameod: Optional frameid, only used if transmit status is desired
        Returns:
          Number of bytes sent
        """
        if not msg:
            return 0

        # hexs = '7E 00 {:02X} 01 {:02X} {:02X} {:02X} {:02X}'.format(
        #     len(msg) + 5,           # LSB (length)
        #     frameid,
        #     (addr & 0xFF00) >> 8,   # Destination address high byte
        #     addr & 0xFF,            # Destination address low byte
        #     options
        # )
        hexs = '7E 00 10 10 01 00 00 00 00 00 00 FF FF FF FE 00 00'
        frame = bytearray.fromhex(hexs)
        #  Append message content
        frame.extend(msg)

        # Calculate checksum byte
        frame.append(0xFF - (sum(frame[3:]) & 0xFF))

        # Escape any bytes containing reserved characters
        # frame = self.Escape(frame)

        # print("Tx: " + self.format(frame))
        return self.serial.write(frame)


    def IRSend(self, msg, addr=0xFFFF, options=0x01, frameid=0x00):
        """
        Inputs:
          msg: A message, in bytes or bytearray format, to be sent to an XBee
          addr: The 16 bit address of the destination XBee
            (default broadcast)
          options: Optional byte to specify transmission options
            (default 0x01: disable ACK)
          frameod: Optional frameid, only used if transmit status is desired
        Returns:
          Number of bytes sent
        """

        if not msg:
            return 0

        # hexs = '7E 00 {:02X} 01 {:02X} {:02X} {:02X} {:02X}'.format(
        #     len(msg) + 5,           # LSB (length)
        #     frameid,
        #     (addr & 0xFF00) >> 8,   # Destination address high byte
        #     addr & 0xFF,            # Destination address low byte
        #     options
        # )
        # hexs = '7E 00 16 10 01 00 00 00 00 00 00 FF FF FF FE 00 00'
        frame = bytearray.fromhex(msg)
        #  Append message content
        #frame.extend(bytearray.fromhex(msg))

        # Calculate checksum byte
        frame.append(0xFF - (sum(frame[3:]) & 0xFF))

        # Escape any bytes containing reserved characters
        # frame = self.Escape(frame)

        print("Tx: " + self.format(frame))

        return self.serial.write(frame)


    def CurrentSend(self, addr=0xFFFF, options=0x01, frameid=0x00):
        # if not msg:
        #     return 0

        # hexs = '7E 00 {:02X} 01 {:02X} {:02X} {:02X} {:02X}'.format(
        #     len(msg) + 5,           # LSB (length)
        #     frameid,
        #     (addr & 0xFF00) >> 8,   # Destination address high byte
        #     addr & 0xFF,            # Destination address low byte
        #     options
        # )     
        hexs = '7E 00 0F 10 01 00 00 00 00 00 00 FF FF FF FE 00 00 70'
        frame = bytearray.fromhex(hexs)
        #  Append message content

        # frame.extend(msg)

        # Calculate checksum byte
        frame.append(0xFF - (sum(frame[3:]) & 0xFF))

        # Escape any bytes containing reserved characters
        # frame = self.Escape(frame)

        # print("Tx: " + self.format(frame))
        return self.serial.write(frame)    

    def LstateSend(self, node_address, addr=0xFFFF, options=0x01, frameid=0x00):
        # if not msg:
        #     return 0

        # hexs = '7E 00 {:02X} 01 {:02X} {:02X} {:02X} {:02X}'.format(
        #     len(msg) + 5,           # LSB (length)
        #     frameid,
        #     (addr & 0xFF00) >> 8,   # Destination address high byte
        #     addr & 0xFF,            # Destination address low byte
        #     options
        # )     
        # hexs = '7E 00 0F 10 01 00 00 00 00 00 00 FF FF FF FE 00 00 70'
        frame = bytearray.fromhex(node_address)
        #  Append message content
        msg = bytearray.fromhex("70")
        frame.extend(msg)

        # Calculate checksum byte
        frame.append(0xFF - (sum(frame[3:]) & 0xFF))

        # Escape any bytes containing reserved characters
        # frame = self.Escape(frame)

        print("Tx: " + self.format(frame))
        return self.serial.write(frame)  

    def Node_One_Send(self, msg, node_address, addr=0xFFFF, options=0x01, frameid=0x00):
        """
        Inputs:
          msg: A message, in bytes or bytearray format, to be sent to an XBee
          addr: The 16 bit address of the destination XBee
            (default broadcast)
          options: Optional byte to specify transmission options
            (default 0x01: disable ACK)
          frameod: Optional frameid, only used if transmit status is desired
        Returns:
          Number of bytes sent
        """
        if not msg:
            return 0

        # hexs = '7E 00 {:02X} 01 {:02X} {:02X} {:02X} {:02X}'.format(
        #     len(msg) + 5,           # LSB (length)
        #     frameid,
        #     (addr & 0xFF00) >> 8,   # Destination address high byte
        #     addr & 0xFF,            # Destination address low byte
        #     options
        # )     
        #hexs = '7E 00 10 10 01 00 13 A2 00 40 EC 3A B7 49 68 00 00'
        frame = bytearray.fromhex(node_address)
        #  Append message content
        frame.extend(msg)

        # Calculate checksum byte
        frame.append(0xFF - (sum(frame[3:]) & 0xFF))

        # Escape any bytes containing reserved characters
        # frame = self.Escape(frame)

        print("Tx: " + self.format(frame))
        return self.serial.write(frame)


    def Unescape(self, msg):
        """
        Helper function to unescaped an XBee API message.

        Inputs:
          msg: An byte or bytearray object containing a raw XBee message
               minus the start delimeter

        Outputs:
          XBee message with original characters.
        """
        if msg[-1] == 0x7D:
            # Last byte indicates an escape, can't unescape that
            return None

        out = bytearray()
        skip = False
        for i in range(len(msg)):
            if skip:
                skip = False
                continue

            if msg[i] == 0x7D:
                out.append(msg[i+1] ^ 0x20)
                skip = True
            else:
                out.append(msg[i])

        return out

    def Escape(self, msg):
        """
        Escapes reserved characters before an XBee message is sent.

        Inputs:
          msg: A bytes or bytearray object containing an original message to
               be sent to an XBee

         Outputs:
           A bytearray object prepared to be sent to an XBee in API mode
         """
        escaped = bytearray()
        reserved = bytearray(b"\x7E\x7D\x11")

        escaped.append(msg[0])
        for m in msg[1:]:   
            if m in reserved:
                escaped.append(0x7D)
                escaped.append(m ^ 0x20)
            else:
                escaped.append(m)

        return escaped

    def format(self, msg):
        """
        Formats a byte or bytearray object into a more human readable string
          where each bytes is represented by two ascii characters and a space

        Input:
          msg: A bytes or bytearray object

        Output:
          A string representation
        """
        return " ".join("{:02x}".format(b) for b in msg)


    def decodeRX(self, msg):
        current1 = int(msg[27:28], 16)
        current2 = int(msg[28:29], 16)
        current3 = int(msg[30:31], 16)
        current4 = int(msg[31:32], 16)
        current = current1*16*16*16+current2*16*16+current3*16+current4
        address = msg[:23].upper()
        temp = dict([["nodeAddress", address],["Current", current]])
        return temp

    def decodeLX(self, msg):
        address = msg[:23].upper()
        state = msg[24:26]
        temp = dict([["nodeAddress", address],["state",state]])
        return temp

    def Statereport(self, msg):
        Msgoutput = []
        Address=[]
        tempformat=[]
        temparray=[]
        state=[]
        Address= msg[3:11]
        state = msg[15:16]
        temparray.extend(Address)
        temparray.extend(state)
        # print("temparray")
        # print(temparray)
        tempformat = self.format(temparray)
        # print("tempformat")
        # print(tempformat)
        Msgoutput = self.decodeLX(tempformat)
        return Msgoutput

    def Currentreport(self, msg):
        Msgoutput = []
        Address=[]
        current=[]
        tempformat=[]
        temparray=[]
        state=[]
        Address= msg[3:11]
        state = msg[15:16]
        current = msg[17:19]
        temparray.extend(Address)
        temparray.extend(state)
        temparray.extend(current)
        # print("temparray")
        # print(temparray)
        tempformat = self.format(temparray)
        # print("tempformat")
        # print(tempformat)
        Msgoutput = self.decodeRX(tempformat)
        return Msgoutput

    def node_N_all_turn(self):
        self.Send(bytearray.fromhex("6E 01"))
        # sleep(2)
        Msg = self.Receive()
        if Msg:
            print("Node N All Open")

    def node_All_turn(self, on):
        if on == 1:
            self.Send(bytearray.fromhex("61 01"))
        elif on == 0:
            self.Send(bytearray.fromhex("61 00"))

        print("Node ALL turn:"+str(on))


    def node_N_one_turn(self, on, node_address):
        node_address = '7E 00 10 10 01 '+ node_address + ' FF FE 00 00' 
        if on == 1:
            self.Node_One_Send(bytearray.fromhex("6E 01"), node_address)
        elif on == 0:
            self.Node_One_Send(bytearray.fromhex("6E 00"), node_address)
        print("Node_N_one_turn")

    def node_L_one_turn(self, state, node_address):
        node_address = '7E 00 10 10 01 '+ node_address + ' FF FE 00 00' 
        if state in range(10):
           turn = "6C 0"+ str(state)
        elif state == 10:
            turn = "6C "+ str(state)
        self.Node_One_Send(bytearray.fromhex(turn), node_address)
        # sleep(1)
        # self.CurrentSend()
        # self.LstateSend(node_address)
        # sleep(1)

        print("Node_L_one_turn")


    def IR_node_send(self, commd):
        power =     "7E 00 16 10 00 00 13 A2 00 40 EC 3A BE FF FE 00 00 72 01 20 00 87 78 EF 10"
        chup =      "7E 00 16 10 00 00 13 A2 00 40 EC 3A BE FF FE 00 00 72 01 20 00 57 A8 EF 10"
        chdown =    "7E 00 16 10 00 00 13 A2 00 40 EC 3A BE FF FE 00 00 72 01 20 00 C7 38 EF 10"
        voiceup =   "7E 00 16 10 00 00 13 A2 00 40 EC 3A BE FF FE 00 00 72 01 20 00 E7 18 EF 10"
        voicedown = "7E 00 16 10 00 00 13 A2 00 40 EC 3A BE FF FE 00 00 72 01 20 00 D7 28 EF 10"
        mute =      "7E 00 16 10 00 00 13 A2 00 40 EC 3A BE FF FE 00 00 72 01 20 00 05 FA EF 10"
        back =      "7E 00 16 10 00 00 13 A2 00 40 EC 3A BE FF FE 00 00 72 01 20 00 07 F8 EF 10"
        tv1 =       "7E 00 16 10 00 00 13 A2 00 40 EC 3A BE FF FE 00 00 72 01 20 00 15 EA EF 10"
        tv2 =       "7E 00 16 10 00 00 13 A2 00 40 EC 3A BE FF FE 00 00 72 01 20 00 0D F2 EF 10"
        tv3 =       "7E 00 16 10 00 00 13 A2 00 40 EC 3A BE FF FE 00 00 72 01 20 00 35 CA EF 10"
        tv4 =       "7E 00 16 10 00 00 13 A2 00 40 EC 3A BE FF FE 00 00 72 01 20 00 95 6A EF 10"
        tv5 =       "7E 00 16 10 00 00 13 A2 00 40 EC 3A BE FF FE 00 00 72 01 20 00 8D 72 EF 10"
        tv6 =       "7E 00 16 10 00 00 13 A2 00 40 EC 3A BE FF FE 00 00 72 01 20 00 85 7A EF 10"
        tv7 =       "7E 00 16 10 00 00 13 A2 00 40 EC 3A BE FF FE 00 00 72 01 20 00 D5 2A EF 10"
        tv8 =       "7E 00 16 10 00 00 13 A2 00 40 EC 3A BE FF FE 00 00 72 01 20 00 CD 32 EF 10"
        tv9 =       "7E 00 16 10 00 00 13 A2 00 40 EC 3A BE FF FE 00 00 72 01 20 00 C5 3A EF 10"
        tv0 =       "7E 00 16 10 00 00 13 A2 00 40 EC 3A BE FF FE 00 00 72 01 20 00 4D B2 EF 10"
        enter =     "7E 00 16 10 00 00 13 A2 00 40 EC 3A BE FF FE 00 00 72 01 20 00 8F 70 EF 10"
        language =  "7E 00 16 10 00 00 13 A2 00 40 EC 3A BE FF FE 00 00 72 01 20 00 45 BA EF 10"
        display =   "7E 00 16 10 00 00 13 A2 00 40 EC 3A BE FF FE 00 00 72 01 20 00 EF 10 EF 10"
        scan =      "7E 00 16 10 00 00 13 A2 00 40 EC 3A BE FF FE 00 00 72 01 20 00 A5 5A EF 10"
        info =      "7E 00 16 10 00 00 13 A2 00 40 EC 3A BE FF FE 00 00 72 01 20 00 AF 50 EF 10"
        energy =    "7E 00 16 10 00 00 13 A2 00 40 EC 3A BE FF FE 00 00 72 01 20 00 2F D0 EF 10"
        boardcast = "7E 00 16 10 00 00 00 00 00 00 00 00 00 FF FE 00 00 72 01 20 00 7F 80 EF 10"

        if commd == 'power':
            print("IRcommd: power")
            self.IRSend(power)
        elif commd == 'chup':
            print("IRcommd: Channel_up")
            self.IRSend(chup)
        elif commd == 'chdown':
            print("IRcommd: Channel_down")
            self.IRSend(chdown)
        elif commd == 'voiceup':
            print("IRcommd: voice_UP")
            self.IRSend(voiceup)
        elif commd == 'voicedown':
            print("IRcommd: voice_down")
            self.IRSend(voicedown)
        elif commd == 'mute':
            print("IRcommd: voice_mute")
            self.IRSend(mute)
        elif commd == 'back':
            print("IRcommd: back")
            self.IRSend(back)
        elif commd == 'tv1':
            print("IRcommd: tv1")
            self.IRSend(tv1)
        elif commd == 'tv2':
            print("IRcommd: tv2")
            self.IRSend(tv2)
        elif commd == 'tv3':
            print("IRcommd: tv3")
            self.IRSend(tv3)
        elif commd == 'tv4':
            print("IRcommd: tv4")
            self.IRSend(tv4)
        elif commd == 'tv5':
            print("IRcommd: tv5")
            self.IRSend(tv5)
        elif commd == 'tv6':
            print("IRcommd: tv6")
            self.IRSend(tv6)
        elif commd == 'tv7':
            print("IRcommd: tv7")
            self.IRSend(tv7)
        elif commd == 'tv8':
            print("IRcommd: tv8")
            self.IRSend(tv8)
        elif commd == 'tv9':
            print("IRcommd: tv9")
            self.IRSend(tv9)
        elif commd == 'tv0':
            print("IRcommd: tv0")
            self.IRSend(tv0)
        elif commd == 'enter':
            print("IRcommd: enter")
            self.IRSend(enter)
        elif commd == 'language':
            print("IRcommd: language")
            self.IRSend(language)
        elif commd == 'display':
            print("IRcommd: display")
            self.IRSend(display)
        elif commd == 'scan':
            print("IRcommd: scan")
            self.IRSend(scan)
        elif commd == 'info':
            print("IRcommd: info")
            self.IRSend(info)
        elif commd == 'energy':
            print("IRcommd: energy")
            self.IRSend(energy)
        elif commd == 'boardcast':
            print("IRcommd: boardcast")
            self.IRSend(boardcast)

        print("Node IR Switch")


    def IR_compare_send(self, pack):

        self.IRSend(pack[:12]+"00 00 13 A2 00 40 EC 3A BE"+pack[39:])
        sleep(0.5)
        print("IR Compare Done")

    def node_all_reset(self):
        node_address = '7E 00 10 17 01 00 00 00 00 00 00 FF FF FF FE' 
        self.Node_One_Send(bytearray.fromhex("02 44 31 04"), node_address)
        sleep(1)
        self.Node_One_Send(bytearray.fromhex("02 44 31 05"), node_address)
        sleep(1)
        # Msg = self.Receive()
        # if Msg:
        #     print("Node_reset_all")
        print("Node_reset_all")


    def node_one_reset(self,node_address):
        node_address = '7E 00 10 17 01'+node_address+'FF FE' 
        self.Node_One_Send(bytearray.fromhex("02 44 31 04"), node_address)
        sleep(0.5)
        self.Node_One_Send(bytearray.fromhex("02 44 31 05"), node_address)
        sleep(0.5)
        # Msg = self.Receive()
        # if Msg:
        #     print("Node_reset_one")
        print("Node_reset_one")


    def Send_P_package(self):
        # self.Send(bytearray.fromhex("70"))
        self.CurrentSend()
        print('Sending P package!!')
        return True
