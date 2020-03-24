class Initialiser:

    def __init__(self):
        self.relays = self.relays()
        self.board_to_room = self.board_to_room()
        self.board_to_bcm = self.board_to_bcm()

    @staticmethod
    def relays():
        return [11, 13, 15, 12, 16, 18, 22]

    @staticmethod
    def board_to_room():
        board_to_room = {
            11: "kitchen",
            13: "no_mans_land",
            15: "bedroom",
            12: "office",
            16: "living",
            18: "bathroom_main",
            20: "bathroom_tiny"
        }
        return board_to_room

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
