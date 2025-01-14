"""
empty.py

Defines the Empty class, representing an empty space on the chessboard.
"""

from .piece import Piece

class Empty(Piece):
    """
    Represents an empty space on the chessboard.

    Inherits from Piece.

    Attributes:
        color (str): The color of the empty space (default: "NA").
        pos (Position): The position of the empty space on the board.
    """

    def __init__(self, color, pos):
        """
        Initializes an Empty object.

        Args:
            color (str): The color of the empty space (default: "NA").
            pos (Position): The position of the empty space.
        """
        super().__init__(color, pos, "empty")
    
    def get_emoji(self):
        return ""
