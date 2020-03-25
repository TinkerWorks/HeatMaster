class Initialiser:

    def __init__(self):
        self.relays = self.relays()
        self.board_to_room = self.board_to_room()
        self.board_to_bcm = self.board_to_bcm()
        self.board_to_room = {
            15: "small bathroom",
            11: "bathroom",
            13: "office",
            12: "livingroom",
            16: "bedroom",
            18: "kitchen",
            22: "no mans land"
        }

    @staticmethod
    def relays():
        return [11, 13, 15, 12, 16, 18, 22]


    def board_to_room(self):
        return self.board_to_room

    def room_to_relay_board( room_name ):
        for relay , room in self.board_to_room:
            if (room == room_name):
                return relay
        raise ValueError('Room name unknown')


    @staticmethod
    def board_to_bcm():
        board_to_bcm = {
            11: 17,
            13: 27,
            15: 22,
            12: 18,
            16: 23,
            18: 24,
            22: 25
        }
        return board_to_bcm
