import enum

class DataType(enum.Enum):
    ClientData = 1
    Handshake = 2
    Terminate = 3
    GetRoom = 4
    StartRec = 5
    StopRec = 6

class Protocol:
    CLIENT_DATA_MIN = 0
    CLIENT_DATA_MAX = 50
    HANDSHAKE = 51
    TERMINATE = 52
    GET_ROOM = 53
    START_REC = 54
    STOP_REC = 55

    typeToOrd = {DataType.ClientData: CLIENT_DATA_MIN, DataType.Handshake: HANDSHAKE, DataType.Terminate: TERMINATE, DataType.GetRoom: GET_ROOM, DataType.StartRec: START_REC, DataType.StopRec: STOP_REC}
    ordToType = {v: k for k, v in typeToOrd.items()}

    def __init__(self, dataType=None, head=None, room=None, data=None, datapacket=None):
        if dataType is not None:
            self.head = Protocol.typeToOrd[dataType]
        else:
            self.head = datapacket[0] if head is None else head
        self.room = datapacket[1] if room is None else room
        self.data = datapacket[2:] if data is None else data
        self.DataType = Protocol.getDataType(self.head)

    @staticmethod
    def getDataType(head):
        if Protocol.CLIENT_DATA_MIN <= head <= Protocol.CLIENT_DATA_MAX:
            return DataType.ClientData
        try:
            return Protocol.ordToType[head]
        except:
            return None

    def out(self):
        bytearr = bytearray(b'')
        bytearr.append(self.head)
        bytearr.append(self.room)
        return bytes(bytearr + self.data)
