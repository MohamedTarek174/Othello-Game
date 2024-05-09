class Player:
    def __init__(self, disks, symbol):
        self.num_of_disks = disks
        self.symbol = symbol

    def Decrement_Disks(self):
        self.num_of_disks -=1
