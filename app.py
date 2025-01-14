from flask import Flask, render_template, request, jsonify
import chess
import chess.engine
from pieces.pawn import Pawn
from pieces.empty import Empty
from pieces.rook import Rook
from pieces.knight import Knight
from pieces.bishop import Bishop
from pieces.queen import Queen
from pieces.king import King
import os
import sys

app = Flask(__name__)

# Initialize the Stockfish engine
STOCKFISH_PATH = "/opt/homebrew/bin/stockfish"  # Update this if Stockfish is installed elsewhere
engine = chess.engine.SimpleEngine.popen_uci(STOCKFISH_PATH)

# Create a persistent chess.Board object to maintain game state
chess_game_board = chess.Board()

# Initialize the chessboard with empty spaces
chess_board = [[Empty("NA", (k + 1, i + 1)) for k in range(8)] for i in range(8)]

# Place pieces on the board
for i in range(8):
    chess_board[1][i] = Pawn("black", (i + 1, 2))  # Black pawns on row 2
    chess_board[6][i] = Pawn("white", (i + 1, 7))  # White pawns on row 7

chess_board[0][0] = Rook("black", (1, 1))
chess_board[0][7] = Rook("black", (8, 1))
chess_board[7][0] = Rook("white", (1, 8))
chess_board[7][7] = Rook("white", (8, 8))

chess_board[0][1] = Knight("black", (2, 1))
chess_board[0][6] = Knight("black", (7, 1))
chess_board[7][1] = Knight("white", (2, 8))
chess_board[7][6] = Knight("white", (7, 8))

chess_board[0][2] = Bishop("black", (3, 1))
chess_board[0][5] = Bishop("black", (6, 1))
chess_board[7][2] = Bishop("white", (3, 8))
chess_board[7][5] = Bishop("white", (6, 8))

chess_board[0][3] = Queen("black", (4, 1))
chess_board[7][3] = Queen("white", (4, 8))

chess_board[0][4] = King("black", (5, 1))
chess_board[7][4] = King("white", (5, 8))


@app.route("/")
def home():
    emoji_board = [
        [(piece.get_emoji(), row_idx, col_idx) for col_idx, piece in enumerate(row)]
        for row_idx, row in enumerate(chess_board)
    ]
    return render_template("template.html", board=emoji_board)


@app.route("/get-valid-moves", methods=["POST"])
def get_valid_moves():
    data = request.get_json()
    row = int(data["row"])
    col = int(data["col"])

    piece = chess_board[row][col]

    # Check if the piece is white and not empty
    if piece.color != "white" or piece.type == "empty":
        return jsonify({"valid_moves": []})

    # Get valid moves for the piece
    valid_moves = valid(piece)

    # Convert valid moves to 0-based indexing
    valid_moves_zero_indexed = [(move[0] - 1, move[1] - 1) for move in valid_moves]

    return jsonify({"valid_moves": valid_moves_zero_indexed})


@app.route("/move-piece", methods=["POST"])
def move_piece():
    data = request.get_json()
    start_row = int(data["start_row"])
    start_col = int(data["start_col"])
    end_row = int(data["end_row"])
    end_col = int(data["end_col"])

    # Convert to 1-based indexing for the move function
    start_pos = (start_col + 1, start_row + 1)
    end_pos = (end_col + 1, end_row + 1)

    # Execute the player's move on the custom chess_board
    move(start_pos, end_pos)

    # Synchronize Stockfish's board with the custom board
    sync_with_stockfish()

    # Debugging: Check whose turn it is
    print(f"After player's move: Turn is {'White' if chess_game_board.turn == chess.WHITE else 'Black'}")

    # Ensure turn is set correctly after the player's move
    if chess_game_board.turn == chess.WHITE:
        print("White just played, it is now Black's turn.")
    else:
        print("Black just played, it is now White's turn.")

    # Ensure turn synchronization: explicitly set the turn to Black after White's move
    if chess_game_board.turn == chess.WHITE:
        print("Turn set to Black after White's move.")
        chess_game_board.turn = chess.BLACK  # Explicitly setting Black's turn

    # Let Stockfish make its move if it's now Black's turn
    if chess_game_board.turn == chess.BLACK:
        print("Triggering Stockfish move...")
        stockfish_move()
    else:
        print("Not Stockfish's turn.")

    # Prepare the updated board for the frontend
    emoji_board = [
        [(piece.get_emoji(), row_idx, col_idx) for col_idx, piece in enumerate(row)]
        for row_idx, row in enumerate(chess_board)
    ]

    return jsonify({"board": emoji_board})


@app.route("/reset-board", methods=["POST"])
def reset_board():
    global chess_board

    # Reinitialize the chessboard with empty spaces
    chess_board = [[Empty("NA", (k + 1, i + 1)) for k in range(8)] for i in range(8)]

    # Place pieces on the board again
    for i in range(8):
        chess_board[1][i] = Pawn("black", (i + 1, 2))  # Black pawns on row 2
        chess_board[6][i] = Pawn("white", (i + 1, 7))  # White pawns on row 7

    chess_board[0][0] = Rook("black", (1, 1))
    chess_board[0][7] = Rook("black", (8, 1))
    chess_board[7][0] = Rook("white", (1, 8))
    chess_board[7][7] = Rook("white", (8, 8))

    chess_board[0][1] = Knight("black", (2, 1))
    chess_board[0][6] = Knight("black", (7, 1))
    chess_board[7][1] = Knight("white", (2, 8))
    chess_board[7][6] = Knight("white", (7, 8))

    chess_board[0][2] = Bishop("black", (3, 1))
    chess_board[0][5] = Bishop("black", (6, 1))
    chess_board[7][2] = Bishop("white", (3, 8))
    chess_board[7][5] = Bishop("white", (6, 8))

    chess_board[0][3] = Queen("black", (4, 1))
    chess_board[7][3] = Queen("white", (4, 8))

    chess_board[0][4] = King("black", (5, 1))
    chess_board[7][4] = King("white", (5, 8))

    # Reset the Stockfish board as well
    sync_with_stockfish()

    # Return the updated board to the frontend directly
    emoji_board = [
        [(piece.get_emoji(), row_idx, col_idx) for col_idx, piece in enumerate(row)]
        for row_idx, row in enumerate(chess_board)
    ]

    return jsonify({"message": "Board has been reset", "board": emoji_board})


def move(start, finish):
    """
    Moves a piece from the start position to the finish position.

    Args:
        start (tuple): The starting position of the piece (x, y).
        finish (tuple): The ending position of the piece (x, y).
    """
    global chess_board
    piece_to_move = chess_board[start[1] - 1][start[0] - 1]

    # Update the piece's position
    piece_to_move.pos = finish

    # If the piece is a pawn, set first_move to False after the first move
    if piece_to_move.type == "pawn":
        piece_to_move.first_move = False

    # Move the piece to the new position on the board
    chess_board[finish[1] - 1][finish[0] - 1] = piece_to_move

    # Replace the old position with an Empty piece
    chess_board[start[1] - 1][start[0] - 1] = Empty("NA", start)


def stockfish_move():
    """
    Uses Stockfish to calculate and execute a move for Black pieces.
    """
    global chess_game_board, chess_board

    # Ensure Stockfish only plays for Black
    if chess_game_board.turn != chess.BLACK:
        print("Error: Stockfish attempted to play out of turn.")
        return

    # Check if the game is over
    if chess_game_board.is_game_over():
        print(f"Game Over: {chess_game_board.result()}")
        return

    try:
        # Let Stockfish calculate the best move for Black
        result = engine.play(chess_game_board, chess.engine.Limit(time=0.1))

        # Debugging: Print Stockfish's move
        print(f"Stockfish intends to move: {result.move}")

        if not result or not result.move:
            print("Error: Stockfish failed to make a move.")
            return

        # Push Stockfish's move to its own board
        chess_game_board.push(result.move)

        # Convert Stockfish move to custom board updates
        from_square = result.move.from_square
        to_square = result.move.to_square

        from_col, from_row = chess.square_file(from_square), chess.square_rank(from_square)
        to_col, to_row = chess.square_file(to_square), chess.square_rank(to_square)

        # Translate to custom board coordinates
        start_pos = (from_col + 1, 8 - from_row)
        end_pos = (to_col + 1, 8 - to_row)

        # Update the custom chess_board
        piece_to_move = chess_board[start_pos[1] - 1][start_pos[0] - 1]

        # If there's a captured piece, we need to clear it
        captured_piece = chess_board[end_pos[1] - 1][end_pos[0] - 1]
        if captured_piece.type != "empty":
            print(f"Captured piece: {captured_piece.type} at {end_pos}")
            chess_board[end_pos[1] - 1][end_pos[0] - 1] = Empty("NA", end_pos)

        # Move the piece
        chess_board[end_pos[1] - 1][end_pos[0] - 1] = piece_to_move
        piece_to_move.pos = end_pos

        # Clear the old position
        chess_board[start_pos[1] - 1][start_pos[0] - 1] = Empty("NA", start_pos)

        # Debugging: Print boards after Stockfish's move
        print("Custom Board after Stockfish move:")
        board_print()
        print("Stockfish Board after move:")
        print(chess_game_board)

        # Ensure turn is properly set after Stockfish's move
        chess_game_board.turn = chess.WHITE if chess_game_board.turn == chess.BLACK else chess.BLACK

        # Sync the custom board with Stockfish's board
        sync_with_stockfish()

    except Exception as e:
        print(f"Error during Stockfish move: {e}")


def sync_with_stockfish():
    """
    Synchronizes the chess_game_board with the custom chess_board.
    """
    global chess_game_board

    # Create a new Stockfish chess.Board object
    chess_game_board.clear()  # Ensure the board is cleared before syncing

    # Mapping emojis to python-chess piece symbols
    emoji_to_symbol = {
        "♟": "p", "♜": "r", "♞": "n", "♝": "b", "♛": "q", "♚": "k",  # Black pieces
        "♙": "P", "♖": "R", "♘": "N", "♗": "B", "♕": "Q", "♔": "K",  # White pieces
    }

    # Set all pieces on the Stockfish board
    for row_idx, row in enumerate(chess_board):
        for col_idx, piece in enumerate(row):
            if piece.type != "empty":  # Only set non-empty pieces
                square = chess.square(col_idx, 7 - row_idx)  # Convert to python-chess square
                symbol = emoji_to_symbol.get(piece.get_emoji(), None)
                if symbol:
                    chess_game_board.set_piece_at(square, chess.Piece.from_symbol(symbol))

    # Explicitly synchronize the turn
    chess_game_board.turn = chess.WHITE if sum(
        piece.color == "white" for row in chess_board for piece in row if piece.type != "empty"
    ) % 2 == 1 else chess.BLACK

    # Debugging: print current turn
    print(f"Syncing turn: {'White' if chess_game_board.turn == chess.WHITE else 'Black'}")


def valid(piece):
    """
    Get all valid moves for the given piece.
    """
    global chess_board
    playable_moves = []
    x, y = piece.pos[0] - 1, piece.pos[1] - 1  # Convert to 0-based index

    if piece.type == "pawn":  # Pawn
        direction = 1 if piece.color == "black" else -1

        # Forward moves
        if 0 <= y + direction < 8 and chess_board[y + direction][x].type == "empty":
            playable_moves.append((x + 1, y + 1 + direction))

        # First-move two-square option
        if piece.first_move and 0 <= y + 2 * direction < 8 and chess_board[y + 2 * direction][x].type == "empty":
            playable_moves.append((x + 1, y + 1 + 2 * direction))

        # Diagonal captures
        for dx in [-1, 1]:
            nx, ny = x + dx, y + direction
            if 0 <= nx < 8 and 0 <= ny < 8:
                target_piece = chess_board[ny][nx]
                if target_piece.type != "empty" and target_piece.color != piece.color:
                    playable_moves.append((nx + 1, ny + 1))

    elif piece.type == "rook":  # Rook
        directions = [(1, 0), (-1, 0), (0, 1), (0, -1)]
        for dx, dy in directions:
            nx, ny = x + dx, y + dy
            while 0 <= nx < 8 and 0 <= ny < 8:
                target_piece = chess_board[ny][nx]
                if target_piece.type == "empty":
                    playable_moves.append((nx + 1, ny + 1))
                elif target_piece.color != piece.color:
                    playable_moves.append((nx + 1, ny + 1))
                    break
                else:
                    break
                nx += dx
                ny += dy

    elif piece.type == "bishop":  # Bishop
        directions = [(1, 1), (1, -1), (-1, 1), (-1, -1)]
        for dx, dy in directions:
            nx, ny = x + dx, y + dy
            while 0 <= nx < 8 and 0 <= ny < 8:
                target_piece = chess_board[ny][nx]
                if target_piece.type == "empty":
                    playable_moves.append((nx + 1, ny + 1))
                elif target_piece.color != piece.color:
                    playable_moves.append((nx + 1, ny + 1))
                    break
                else:
                    break
                nx += dx
                ny += dy

    elif piece.type == "queen":  # Queen
        directions = [(1, 0), (-1, 0), (0, 1), (0, -1), (1, 1), (1, -1), (-1, 1), (-1, -1)]
        for dx, dy in directions:
            nx, ny = x + dx, y + dy
            while 0 <= nx < 8 and 0 <= ny < 8:
                target_piece = chess_board[ny][nx]
                if target_piece.type == "empty":
                    playable_moves.append((nx + 1, ny + 1))
                elif target_piece.color != piece.color:
                    playable_moves.append((nx + 1, ny + 1))
                    break
                else:
                    break
                nx += dx
                ny += dy

    elif piece.type == "knight":  # Knight
        for dx, dy in [(2, 1), (2, -1), (-2, 1), (-2, -1), (1, 2), (1, -2), (-1, 2), (-1, -2)]:
            nx, ny = x + dx, y + dy
            if 0 <= nx < 8 and 0 <= ny < 8:
                target_piece = chess_board[ny][nx]
                if target_piece.type == "empty" or target_piece.color != piece.color:
                    playable_moves.append((nx + 1, ny + 1))

    elif piece.type == "king":  # King
        for dx, dy in [(1, 0), (-1, 0), (0, 1), (0, -1), (1, 1), (1, -1), (-1, 1), (-1, -1)]:
            nx, ny = x + dx, y + dy
            if 0 <= nx < 8 and 0 <= ny < 8:
                target_piece = chess_board[ny][nx]
                if target_piece.type == "empty" or target_piece.color != piece.color:
                    playable_moves.append((nx + 1, ny + 1))

    return playable_moves


def board_print():
    """
    Prints both the custom board and the Stockfish board for debugging.
    """
    print("Custom Board:")
    for row in chess_board:
        print(" ".join([piece.get_name() for piece in row]))
    print("\nStockfish Board:")
    print(chess_game_board)
    print("\n")


if __name__ == "__main__":
    app.run(debug=True, port=5001)
