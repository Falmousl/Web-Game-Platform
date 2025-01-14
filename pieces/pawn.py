"""
pawn.py

Defines the Pawn class, a subclass of Piece.
"""

from .piece import Piece

class Pawn(Piece):
    """
    Represents a pawn chess piece.

    Inherits from Piece.

    Attributes:
        color (str): The color of the pawn ('white' or 'black').
        pos (tuple): The position of the pawn on the board.
        first_move (bool): Indicates if the pawn has made its first move.
    """

    def __init__(self, color, pos):
        """
        Initializes a Pawn object.

        Args:
            color (str): The color of the pawn.
            pos (tuple): The position of the pawn (x, y).
        """
        super().__init__(color, pos, "pawn")
        self.first_move = True  # Track if the pawn has moved yet

    def get_potential_moves(self):
        """
        Calculates all potential moves for the pawn.

        This includes forward moves and diagonal captures without filtering.

        Returns:
            list[tuple]: A list of potential moves as (x, y) tuples.
        """
        moves = []
        direction = 1 if self.color == "black" else -1  # Black moves down, white moves up

        # Forward move (1 square)
        moves.append((self.pos[0], self.pos[1] + direction))

        # Forward move (2 squares) if first move
        if self.first_move:
            moves.append((self.pos[0], self.pos[1] + 2 * direction))

        # Diagonal capture moves
        moves.append((self.pos[0] - 1, self.pos[1] + direction))  # Left diagonal
        moves.append((self.pos[0] + 1, self.pos[1] + direction))  # Right diagonal

        return moves

    def set_position(self, new_pos):
        """
        Updates the pawn's position and sets first_move to False after the first move.

        Args:
            new_pos (tuple): The new position of the pawn (x, y).
        """
        self.pos = new_pos
        self.first_move = False  # Mark that the pawn has moved

    def get_emoji(self):
        return "♙" if self.color == "white" else "♟"

