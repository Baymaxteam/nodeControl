
import serial
from collections import deque
from time import sleep

class XBee():
    RxBuff = bytearray()
    RxMessages = deque()

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

        # All bytes in message must be unescaped before validating content
        frame = self.Unescape(msg)

        LSB = frame[1]
        # Frame (minus checksum) must contain at least length equal to LSB
        if LSB > (len(frame[2:]) - 1):
            return False

        # Validate checksum
        if (sum(frame[2:3+LSB]) & 0xFF) != 0xFF:
            return False

        print("Rx: " + self.format(bytearray(b'\x7E') + msg))
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

        print("Tx: " + self.format(frame))
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
        hexs = '7E 00 16 10 01 00 00 00 00 00 00 FF FF FF FE 00 00'
        frame = bytearray.fromhex(hexs)
        #  Append message content
        frame.extend(msg)

        # Calculate checksum byte
        frame.append(0xFF - (sum(frame[3:]) & 0xFF))

        # Escape any bytes containing reserved characters
        frame = self.Escape(frame)

        print("Tx: " + self.format(frame))
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
        temp = dict([["nodeAddress", msg[:30]],
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
        j = len(Msg)
        #print(j)
        while i < j:
            temparray=[]
            MsgPopleft = Msg.popleft()
            Address= MsgPopleft[3:13]
            current = MsgPopleft[17:19]
            temparray.extend(Address)
            temparray.extend(current)
            #print(temparray)
            tempformat = self.format(temparray)
            print(tempformat)
            Msgoutput = self.decodeRX(Msgoutput, tempformat)
            i += 1
        #print(Msgoutput)
        return Msgoutput
        i=0
        j=0
    def node_N_all_open(self):
        self.Send(bytearray.fromhex("6E 01"))
        sleep(1)
        Msg = self.Receive()
        if Msg:
            print("Node N All Open")

    def node_N_all_close(self):
        self.Send(bytearray.fromhex("6E 00"))
        sleep(1)
        Msg = self.Receive()
        if Msg:
            print("Node N All Close")

    def node_All_open(self):
        self.Send(bytearray.fromhex("61 01"))
        sleep(1)
        Msg = self.Receive()
        if Msg:
            print("Node ALL Open")

    def node_All_close(self):
        self.Send(bytearray.fromhex("61 00"))
        sleep(1)
        Msg = self.Receive()
        if Msg:
            print("Node ALL Close")

    def node_N_one_open(self, node_address):
        self.Node_One_Send(bytearray.fromhex("6E 01"), node_address)
        sleep(1)
        Msg = self.Receive()
        if Msg:
            print("Node_N_one_open")

    def node_N_one_close(self, node_address):
        self.Node_One_Send(bytearray.fromhex("6E 00"), node_address)
        sleep(1)
        Msg = self.Receive()
        if Msg:
            print("Node_N_one_close")