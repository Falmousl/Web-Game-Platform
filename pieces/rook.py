"""
rook.py

Defines the Rook class, a subclass of Piece.
"""

from .piece import Piece

class Rook(Piece):
    """
    Represents a rook chess piece.

    Inherits from Piece.

    Attributes:
        color (str): The color of the rook ('white' or 'black').
        pos (tuple): The position of the rook on the board.
    """

    def __init__(self, color, pos):
        """
        Initializes a Rook object.

        Args:
            color (str): The color of the rook.
            pos (tuple): The position of the rook (x, y).
        """
        super().__init__(color, pos, "rook")

    def get_potential_moves(self):
        """
        Calculates the rook's potential moves.

        Returns:
            list[tuple]: A list of potential moves as (x, y) tuples.
        """
        moves = []
        for i in range(8):
            if (i + 1 != self.pos[0]):
                moves.append((i + 1, self.pos[1]))
        for i in range(8):
            if (i + 1 != self.pos[1]):
                moves.append((self.pos[0], i + 1))
        return moves
    
    def get_emoji(self):
        return "♖" if self.color == "white" else "♜"
