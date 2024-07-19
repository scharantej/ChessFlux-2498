
from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

board = [
    ['r', 'n', 'b', 'q', 'k', 'b', 'n', 'r'],
    ['p', 'p', 'p', 'p', 'p', 'p', 'p', 'p'],
    ['.', '.', '.', '.', '.', '.', '.', '.'],
    ['.', '.', '.', '.', '.', '.', '.', '.'],
    ['.', '.', '.', '.', '.', '.', '.', '.'],
    ['.', '.', '.', '.', '.', '.', '.', '.'],
    ['P', 'P', 'P', 'P', 'P', 'P', 'P', 'P'],
    ['R', 'N', 'B', 'Q', 'K', 'B', 'N', 'R'],
]

turn = 'white'

@app.route('/')
def home():
    return render_template('index.html', board=board)

@app.route('/move', methods=['POST'])
def move():
    global board, turn

    data = request.get_json()
    start_row, start_col, end_row, end_col = data['start'], data['startCol'], data['end'], data['endCol']

    if board[start_row][start_col] == '.':
        return jsonify({'error': 'No piece at starting position'})

    if turn == 'white' and board[start_row][start_col].islower():
        return jsonify({'error': 'Not your turn'})

    if turn == 'black' and board[start_row][start_col].isupper():
        return jsonify({'error': 'Not your turn'})

    if not is_valid_move(board, turn, start_row, start_col, end_row, end_col):
        return jsonify({'error': 'Invalid move'})

    board[end_row][end_col] = board[start_row][start_col]
    board[start_row][start_col] = '.'

    turn = 'white' if turn == 'black' else 'black'

    return jsonify({'board': board})

@app.route('/check', methods=['POST'])
def check():
    global board, turn

    data = request.get_json()
    king_row, king_col = data['kingRow'], data['kingCol']

    if board[king_row][king_col] != turn.upper() + 'K':
        return jsonify({'error': 'Invalid king position'})

    return jsonify({'in_check': is_in_check(board, turn, king_row, king_col)})

@app.route('/reset', methods=['POST'])
def reset():
    global board, turn

    board = [
        ['r', 'n', 'b', 'q', 'k', 'b', 'n', 'r'],
        ['p', 'p', 'p', 'p', 'p', 'p', 'p', 'p'],
        ['.', '.', '.', '.', '.', '.', '.', '.'],
        ['.', '.', '.', '.', '.', '.', '.', '.'],
        ['.', '.', '.', '.', '.', '.', '.', '.'],
        ['.', '.', '.', '.', '.', '.', '.', '.'],
        ['P', 'P', 'P', 'P', 'P', 'P', 'P', 'P'],
        ['R', 'N', 'B', 'Q', 'K', 'B', 'N', 'R'],
    ]

    turn = 'white'

    return jsonify({'board': board})

def is_valid_move(board, turn, start_row, start_col, end_row, end_col):
    piece = board[start_row][start_col]

    if piece == '.':
        return False

    if turn == 'white' and piece.islower():
        return False

    if turn == 'black' and piece.isupper():
        return False

    if piece == 'p':
        if turn == 'white':
            if start_row == 6 and end_row == 4 and end_col == start_col:
                return True
            elif end_row == start_row - 1 and end_col == start_col:
                return True
            elif end_row == start_row - 1 and abs(end_col - start_col) == 1 and board[end_row][end_col].islower():
                return True
        else:
            if start_row == 1 and end_row == 3 and end_col == start_col:
                return True
            elif end_row == start_row + 1 and end_col == start_col:
                return True
            elif end_row == start_row + 1 and abs(end_col - start_col) == 1 and board[end_row][end_col].isupper():
                return True

    elif piece == 'r':
        if end_row == start_row or end_col == start_col:
            for i in range(min(end_row, start_row) + 1, max(end_row, start_row)):
                if board[i][start_col] != '.':
                    return False
            for i in range(min(end_col, start_col) + 1, max(end_col, start_col)):
                if board[start_row][i] != '.':
                    return False
            return True

    elif piece == 'n':
        if (abs(end_row - start_row) == 2 and abs(end_col - start_col) == 1) or (abs(end_row - start_row) == 1 and abs(end_col - start_col) == 2):
            return True

    elif piece == 'b':
        if abs(end_row - start_row) == abs(end_col - start_col):
            for i in range(1, abs(end_row - start_row)):
                if end_row > start_row:
                    if end_col > start_col:
                        if board[start_row + i][start_col + i] != '.':
                            return False
                    else:
                        if board[start_row + i][start_col - i] != '.':
                            return False
                else:
                    if end_col > start_col:
                        if board[start_row - i][start_col + i] != '.':
                            return False
                    else:
                        if board[start_row - i][start_col - i] != '.':
                            return False
            return True

    elif piece == 'q':
        if end_row == start_row or end_col == start_col:
            for i in range(min(end_row, start_row) + 1, max(end_row, start_row)):
                if board[i][start_col] != '.':
                    return False
            for i in range(min(end_col, start_col) + 1, max(end_col, start_col)):
                if board[start_row][i] != '.':
                    return False
            return True
        elif abs(end_row - start_row) == abs(end_col - start_col):
            for i in range(1, abs(end_row - start_row)):
                if end_row > start_row:
                    if end_col > start_col:
                        if board[start_row + i][start_col + i] != '.':
                            return False
                    else:
                        if board[start_row + i][start_col - i] != '.':
                            return False
                else:
                    if end_col > start_col:
                        if board[start_row - i][start_col + i] != '.':
                            return False
                    else:
                        if board[start_row - i][start_col - i] != '.':
                            return False
            return True

    elif piece == 'k':
        if abs(end_row - start_row) <= 1 and abs(end_col - start_col) <= 1:
            return True

    return False

def is_in_check(board, turn, king_row, king_col):
    for i in range(8):
        for j in range(8):
            if board[i][j] != '.' and board[i][j].lower() != turn:
                if is_valid_move(board, board[i][j].lower(), i, j, king_row, king_col):
                    return True

    return False

if __name__ == '__main__':
    app.run(debug=True)
