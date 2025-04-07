class Player:
    def __init__(self, player_tuple):
        self.nflId = player_tuple[0]
        self.height = player_tuple[1]
        self.weight = player_tuple[2]
        self.birthday = player_tuple[3]
        self.college = player_tuple[4]
        self.position = player_tuple[5]
        self.displayName = player_tuple[6]
        self.name = self.displayName

