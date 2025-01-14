"""
piece.py

Defines the base Piece class for managing chess pieces on the board.
"""

class Piece:
    """
    Represents a generic chess piece.

    Attributes:
        color (str): The color of the piece ('white' or 'black').
        type (str): The type of the piece (e.g., 'pawn', 'empty').
        pos (tuple): The position of the piece on the board as (x, y).
    """

    def __init__(self, color, pos, type):
        """
        Initializes a Piece object.

        Args:
            color (str): The color of the piece.
            pos (tuple): The position of the piece (x, y).
            type (str): The type of the piece.
        """
        self.color = color
        self.type = type
        self.pos = pos

    def get_potential_moves(self):
        """
        Placeholder for calculating the piece's potential moves.

        Raises:
            NotImplementedError: Should be overridden by subclasses.
        """
        raise NotImplementedError("This method should be overridden by subclasses")

    def get_name(self):
        """
        Returns a string representation of the piece.

        Returns:
            str: A string showing the piece's color and type, or empty brackets if it is empty.
        """
        if self.type == "empty":
            return "[    ]"
        else:
            return f"[{self.color[0]}{self.type[:3]}]"

    def get_position(self):
        """
        Gets the position of the piece.

        Returns:
            tuple: The current position of the piece as (x, y).
        """
        return self.pos
    
    def get_emoji(self):
        raise NotImplementedError("This method should be overridden by subclasses")
