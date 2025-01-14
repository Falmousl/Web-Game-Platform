"""
knight.py

Defines the Knight class, a subclass of Piece.
"""

from .piece import Piece

class Knight(Piece):
    """
    Represents a knight chess piece.

    Inherits from Piece.

    Attributes:
        color (str): The color of the knight ('white' or 'black').
        pos (tuple): The position of the knight on the board.
    """

    def __init__(self, color, pos):
        """
        Initializes a Knight object.

        Args:
            color (str): The color of the knight.
            pos (tuple): The position of the knight (x, y).
        """
        super().__init__(color, pos, "knight")

    def get_potential_moves(self):
        """
        Calculates the knight's potential moves.

        Returns:
            list[tuple]: A list of potential moves as (x, y) tuples.
        """
        moves = [(self.pos[0] - 1, self.pos[1] - 2), (self.pos[0] - 2, self.pos[1] - 1),
                 (self.pos[0] + 1, self.pos[1] - 2), (self.pos[0] + 2, self.pos[1] - 1),
                 (self.pos[0] - 2, self.pos[1] + 1), (self.pos[0] - 1, self.pos[1] + 2),
                 (self.pos[0] + 2, self.pos[1] + 1), (self.pos[0] + 1, self.pos[1] + 2)]
        return moves
    
    def get_emoji(self):
        return "♘" if self.color == "white" else "♞"
