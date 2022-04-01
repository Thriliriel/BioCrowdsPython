
class MarkerClass:
    def __init__(self, position):
        self.position = position
        self.minDistance = 5
        self.taken = False
        self.owner = None

    def ResetMarker(self):
        self.minDistance = 5
        self.taken = False
        self.owner = None