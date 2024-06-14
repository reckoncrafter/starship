class PlayerDied(Exception):
    def __init__(self, reason):
        self.reason = reason
    
    def __str__(self):
        return f"You have died from {self.reason}"

class PlayerCommittedSuicide(PlayerDied):
    def __str__(self):
        return f"You have killed yourself via {self.reason}"