class PerdudoExcept(Exception):
    pass

class PerudoWinner(PerdudoExcept):
    def __init__(self, message, player_id):
        # Call the base class constructor with the parameters it needs
        super().__init__(message, player_id)