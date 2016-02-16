
import serial
from collections import deque
from time import sleep

class XBee():
    RxBuff = bytearray()
    RxMessages = deque()

    node_address ={'00 13 A2 00 40 EC 3A A4':'Nnode1', '00 13 A2 00 40 EC 3A B7':'Nnode2', 
                   '00 13 A2 00 40 EC 3A 97':'Nnode3', '00 13 A2 00 40 B3 2D 41':'Nnode4',
                   '00 13 A2 00 40 EC 3A 98':'Nnode5', '00 13 A2 00 40 B3 31 65':'Nnode6',
                   '00 13 A2 00 40 B3 2D 4F':'Lnode1', '00 13 A2 00 40 B3 2D 5B':'Lnode2',
                   '00 13 A2 00 40 C2 8B B7':'IRnode'}
                   
    def __init__(self, serialport, baudrate=9600):
        self.serial = serial.Serial(port=serialport, baudrate=baudrate)

    def Receive(self):
        """
           Receives data from serial and checks buffer for potential messages.
           Returns the next message in the queue if available.
        """
        self.RxMessages.clear()
        remaining = self.serial.inWaiting()
        while remaining:
            chunk = self.serial.read(remaining)
            remaining -= len(chunk)
            self.RxBuff.extend(chunk)

        msgs = self.RxBuff.split(bytes(b'\x7E'))

        for msg in msgs[:-1]:
            if(len(msg)>0): # 避免空的訊息
                self.Validate(msg)

        self.RxBuff = (bytearray() if self.Validate(msgs[-1]) else msgs[-1])

        if self.RxMessages:
            return self.RxMessages
           #return self.RxMessages.popleft()
        else:
            return None

    def Validate(self, msg):
        """
        Parses a byte or bytearray object to verify the contents are a
          properly formatted XBee message.

        Inputs: An incoming XBee message

        Outputs: True or False, indicating message validity
        """
        # 9 bytes is Minimum length to be a valid Rx frame
        #  LSB, MSB, Type, Source Address(2), RSSI,
        #  Options, 1 byte data, checksum
        if (len(msg) - msg.count(bytes(b'0x7D'))) < 9:
            return False

       # print('msg:{0}'.format(msg))
        # All bytes in message must be unescaped before validating content
        frame = self.Unescape(msg)
        # print('frame:{0}'.format(frame))
        if(frame == None):
            return False
        LSB = frame[1]
        # Frame (minus checksum) must contain at least length equal to LSB
        if LSB > (len(frame[2:]) - 1):
            return False

        # Validate checksum
        if (sum(frame[2:3+LSB]) & 0xFF) != 0xFF:
            return False

        # print("Rx: " + self.format(bytearray(b'\x7E') + msg))
        self.RxMessages.append(frame)
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
        frame = self.Escape(frame)

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

        # print("Tx: " + self.format(frame))
        return self.serial.write(frame)


    def CurrentSend(self, msg, addr=0xFFFF, options=0x01, frameid=0x00):
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
        hexs = '7E 00 0F 10 00 00 00 00 00 00 00 FF FF FF FE 00 00'
        frame = bytearray.fromhex(hexs)
        #  Append message content
        frame.extend(msg)

        # Calculate checksum byte
        frame.append(0xFF - (sum(frame[3:]) & 0xFF))

        # Escape any bytes containing reserved characters
        frame = self.Escape(frame)

        # print("Tx: " + self.format(frame))
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
        frame = self.Escape(frame)

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


    def decodeRX(self, data, msg):
        current1 = int(msg[30:31], 16)
        current2 = int(msg[31:32], 16)
        current3 = int(msg[33:34], 16)
        current4 = int(msg[34:35], 16)
        current = current1*16*16*16+current2*16*16+current3*16+current4
        address = msg[:23].upper()
        temp = dict([["nodeAddress", address],
                     ["Contect", current]])
        data.append(temp)
        return data


    def Currentreport(self):
        Msgoutput = []
        MsgPopleft = []
        Address=[]
        current=[]
        tempformat=[]
        self.CurrentSend(bytearray.fromhex("70"))
        sleep(5)
        Msg = self.Receive()
        i = 0
        try:
            j = len(Msg)
        except:
            return('Nothing return')

        while i < j:
            temparray=[]
            MsgPopleft = Msg.popleft()
            Address= MsgPopleft[3:13] 
            current = MsgPopleft[17:19]
            temparray.extend(Address)
            temparray.extend(current)
            #print(temparray)
            tempformat = self.format(temparray)
            # print(tempformat)
            Msgoutput = self.decodeRX(Msgoutput, tempformat)
            i += 1
        #print(Msgoutput)
        return Msgoutput
        i=0
        j=0


    def node_N_all_turn(self):
        self.Send(bytearray.fromhex("6E 01"))
        sleep(2)
        Msg = self.Receive()
        if Msg:
            print("Node N All Open")

    # def node_N_all_close(self):
    #     self.Send(bytearray.fromhex("6E 00"))
    #     sleep(2)
    #     Msg = self.Receive()
    #     if Msg:
    #         print("Node N All Close")

    def node_All_turn(self, on):
        if on == 1:
            self.Send(bytearray.fromhex("61 01"))
        elif on == 0:
            self.Send(bytearray.fromhex("61 00"))
        sleep(2)
        Msg = self.Receive()
        if Msg:
            print("Node ALL turn:"+str(on))

    # def node_All_close(self):
    #     self.Send(bytearray.fromhex("61 00"))
    #     sleep(2)
    #     Msg = self.Receive()
    #     if Msg:
    #         print("Node ALL Close")

    def node_N_one_turn(self, on, node_address):
        node_address = '7E 00 10 10 01 '+ node_address + ' FF FE 00 00' 
        if on == 1:
            self.Node_One_Send(bytearray.fromhex("6E 01"), node_address)
        elif on == 0:
            self.Node_One_Send(bytearray.fromhex("6E 00"), node_address)
        sleep(2)
        Msg = self.Receive()
        if Msg:
            print("Node_N_one_turn")

    # def node_N_one_close(self, node_address):
    #     self.Node_One_Send(bytearray.fromhex("6E 00"), node_address)
    #     sleep(2)
    #     Msg = self.Receive()
    #     if Msg:
    #         print("Node_N_one_close")

    def node_L_one_turn(self, state, node_address):
        node_address = '7E 00 10 10 01 '+ node_address + ' FF FE 00 00' 
        if state in range(10):
           turn = "6C 0"+ str(state)
        elif state == 10:
            turn = "6C "+ str(state)
        self.Node_One_Send(bytearray.fromhex(turn), node_address)
        sleep(2)
        Msg = self.Receive()
        try:
            if Msg:
                print("Node_L_one_turn")
        except:
            print('Nothing return')


    def IR_node_send(self, commd):
        on1 = '7E 00 52 10 01 00 13 A2 00 40 C2 8B B7 FF FE 00 00 72 00 02 02 FC 21 C6 11 C2 01 8A 02 C2 01 D6 06 C2 01 8A 02 C2 01 BC 02 90 01 BC 02 90 01 BC 02 C2 01 8A 02 90 01 BC 02 C2 01 D6 06 C2 01 8A 02 C2 01 08 07 90 01 08 07 C2 01 D6 06 C2 01 D6 06 C2 01 8A 02'
        on2 = '7E 00 52 10 01 00 13 A2 00 40 C2 8B B7 FF FE 00 00 72 00 02 01 C2 01 08 07 90 01 BC 02 90 01 BC 02 C2 01 D6 06 C2 01 8A 02 C2 01 D6 06 C2 01 8A 02 C2 01 8A 02 C2 01 BC 02 90 01 08 07 C2 01 D6 06 C2 01 8A 02 C2 01 D6 06 C2 01 BC 02 90 01 D6 06 F4 01 D6 06'
        on3 = '7E 00 1A 10 01 00 13 A2 00 40 C2 8B B7 FF FE 00 00 72 00 02 00 43 00 C2 01 D6 06 C2 01'
        up1 = '7E 00 52 10 01 00 13 A2 00 40 C2 8B B7 FF FE 00 00 72 00 02 02 92 22 94 11 F4 01 8A 02 90 01 08 07 F4 01 8A 02 90 01 BC 02 C2 01 8A 02 C2 01 BC 02 90 01 BC 02 C2 01 8A 02 C2 01 08 07 C2 01 8A 02 C2 01 08 07 90 01 08 07 C2 01 D6 06 F4 01 D6 06 C2 01 8A 02'
        up2 = '7E 00 52 10 01 00 13 A2 00 40 C2 8B B7 FF FE 00 00 72 00 02 01 C2 01 08 07 C2 01 8A 02 C2 01 08 07 C2 01 8A 02 C2 01 8A 02 C2 01 08 07 C2 01 8A 02 C2 01 BC 02 90 01 BC 02 C2 01 D6 06 C2 01 8A 02 F4 01 D6 06 C2 01 08 07 C2 01 8A 02 C2 01 08 07 90 01 08 07'
        up3 = '7E 00 1A 10 01 00 13 A2 00 40 C2 8B B7 FF FE 00 00 72 00 02 00 43 00 C2 01 D6 06 C2 01 '
        mu1 = '7E 00 52 10 01 00 13 A2 00 40 C2 8B B7 FF FE 00 00 72 00 02 02 FC 21 C6 11 C2 01 8A 02 C2 01 08 07 90 01 8A 02 C2 01 BC 02 C2 01 8A 02 90 01 BC 02 C2 01 8A 02 C2 01 8A 02 C2 01 D6 06 C2 01 BC 02 90 01 08 07 C2 01 D6 06 C2 01 D6 06 C2 01 D6 06 C2 01 BC 02'
        mu2 = '7E 00 52 10 01 00 13 A2 00 40 C2 8B B7 FF FE 00 00 72 00 02 01 90 01 08 07 C2 01 8A 02 90 01 BC 02 C2 01 D6 06 C2 01 D6 06 C2 01 BC 02 90 01 BC 02 90 01 BC 02 C2 01 8A 02 C2 01 D6 06 C2 01 D6 06 C2 01 BC 02 90 01 BC 02 90 01 08 07 C2 01 D6 06 C2 01 D6 06'
        mu3 = '7E 00 1A 10 01 00 13 A2 00 40 C2 8B B7 FF FE 00 00 72 00 02 00 43 00 C2 01 08 07 90 01'
        
        if commd == 'ON':
            print("IRcommd: ON")
            self.IRSend(on1)
            sleep(0.5)
            self.IRSend(on2)
            sleep(0.5)
            self.IRSend(on3)
            sleep(0.5)


        elif commd == 'UP':
            print("IRcommd: UP")
            self.IRSend(up1)
            sleep(0.5)
            self.IRSend(up2)
            sleep(0.5)
            self.IRSend(up3)
            sleep(0.5)

        elif commd == 'MUTE':
            print("IRcommd: MUTE")
            self.IRSend(mu1)
            sleep(0.1)
            self.IRSend(mu2)
            sleep(0.1)
            self.IRSend(mu3)
            sleep(0.1)
            self.IRSend(mu3)
            sleep(0.1)

        sleep(2)
        Msg = self.Receive()
        try:
            if Msg:
                print("Node IR Switch")
        except:
            print('Nothing return')


    def node_all_reset(self):
        node_address = '7E 00 10 17 01 00 00 00 00 00 00 FF FF FF FE' 
        self.Node_One_Send(bytearray.fromhex("02 44 31 04"), node_address)
        sleep(1)
        self.Node_One_Send(bytearray.fromhex("02 44 31 05"), node_address)
        sleep(1)
        Msg = self.Receive()
        if Msg:
            print("Node_reset_all")

    def node_one_reset(self,node_address):
        node_address = '7E 00 10 17 01'+node_address+'FF FE' 
        self.Node_One_Send(bytearray.fromhex("02 44 31 04"), node_address)
        sleep(1)
        self.Node_One_Send(bytearray.fromhex("02 44 31 05"), node_address)
        sleep(1)
        Msg = self.Receive()
        if Msg:
            print("Node_reset_one")



