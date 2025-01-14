"""
king.py

Defines the King class, a subclass of Piece.
"""

from .piece import Piece

class King(Piece):
    """
    Represents a king chess piece.

    Inherits from Piece.

    Attributes:
        color (str): The color of the king ('white' or 'black').
        pos (tuple): The position of the king on the board.
    """

    def __init__(self, color, pos):
        """
        Initializes a King object.

        Args:
            color (str): The color of the king.
            pos (tuple): The position of the king (x, y).
        """
        super().__init__(color, pos, "king")

    def get_potential_moves(self):
        """
        Calculates the king's potential moves.

        Returns:
            list[tuple]: A list of potential moves as (x, y) tuples.
        """
        moves = [(self.pos[0], self.pos[1] - 1),
                 (self.pos[0] + 1, self.pos[1] - 1),
                 (self.pos[0] + 1, self.pos[1]),
                 (self.pos[0] + 1, self.pos[1] + 1),
                 (self.pos[0], self.pos[1] + 1),
                 (self.pos[0] - 1, self.pos[1] + 1),
                 (self.pos[0] - 1, self.pos[1]),
                 (self.pos[0] - 1, self.pos[1] - 1)]

        return moves
    
    def get_emoji(self):
        return "♔" if self.color == "white" else "♚"
