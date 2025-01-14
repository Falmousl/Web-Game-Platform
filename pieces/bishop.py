"""
bishop.py

Defines the Bishop class, a subclass of Piece.
"""

from .piece import Piece

class Bishop(Piece):
    """
    Represents a bishop chess piece.

    Inherits from Piece.

    Attributes:
        color (str): The color of the bishop ('white' or 'black').
        pos (tuple): The position of the bishop on the board.
    """

    def __init__(self, color, pos):
        """
        Initializes a Bishop object.

        Args:
            color (str): The color of the bishop.
            pos (tuple): The position of the bishop (x, y).
        """
        super().__init__(color, pos, "bishop")

    def get_potential_moves(self):
        """
        Calculates the bishop's potential moves.

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
        
        return moves
    
    
    def get_emoji(self):
        return "♗" if self.color == "white" else "♝"

