"""
queen.py

Defines the Queen class, a subclass of Piece.
"""

from .piece import Piece

class Queen(Piece):
    """
    Represents a queen chess piece.

    Inherits from Piece.

    Attributes:
        color (str): The color of the queen ('white' or 'black').
        pos (tuple): The position of the queen on the board.
    """

    def __init__(self, color, pos):
        """
        Initializes a Queen object.

        Args:
            color (str): The color of the queen.
            pos (tuple): The position of the queen (x, y).
        """
        super().__init__(color, pos, "queen")

    def get_potential_moves(self):
        """
        Calculates the queen's potential moves.

        Returns:
            list[tuple]: A list of potential moves as (x, y) tuples.
        """
        moves = []

        i = 1
        while(self.pos[0] + i <= 8 and self.pos[1] - i >= 1):
            moves.append((self.pos[0] + i, self.pos[1] - i))
            i += 1
        
        i = 1
        while(self.pos[0] - i >= 1 and self.pos[1] - i >= 1):
            moves.append((self.pos[0] - i, self.pos[1] - i))
            i += 1
        
        i = 1
        while(self.pos[0] + i <= 8 and self.pos[1] + i <= 8):
            moves.append((self.pos[0] + i, self.pos[1] + i))
            i += 1
        
        i = 1
        while(self.pos[0] - i >= 1 and self.pos[1] + i <= 8):
            moves.append((self.pos[0] - i, self.pos[1] + i))
            i += 1
        
        for i in range(8):
            if (i + 1 != self.pos[0]):
                moves.append((i + 1, self.pos[1]))
        for i in range(8):
            if (i + 1 != self.pos[1]):
                moves.append((self.pos[0], i + 1))

        
        return moves
    
    def get_emoji(self):
        return "♕" if self.color == "white" else "♛"
    
    
