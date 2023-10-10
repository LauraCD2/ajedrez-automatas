from flask import Flask, render_template, request, jsonify


app = Flask(__name__)

class Piece:
    def __init__(self, color):
        self.color = color

    def symbol(self):
        return ''

    def valid_moves(self, current_position, board):
        return []

# Las clases individuales de piezas van aquí

# Pawn (Peón)
class Pawn(Piece):
    def valid_moves(self, current_position, board):
        x, y = current_position
        moves = []

        # Movimiento básico hacia adelante
        forward = -1 if self.color == 'white' else 1
        if 0 <= x + forward < 8 and not board[x + forward][y]:
            moves.append((x + forward, y))
            
            # Doble avance inicial
            if (self.color == 'white' and x == 6) or (self.color == 'black' and x == 1):
                if not board[x + 2 * forward][y]:
                    moves.append((x + 2 * forward, y))

        # Capturas diagonales
        for dy in [-1, 1]:
            if 0 <= y + dy < 8:
                target = board[x + forward][y + dy]
                if target and target.color != self.color:  # Hay una pieza oponente en diagonal
                    moves.append((x + forward, y + dy))

        return moves

# Rook (Torre)
class Rook(Piece):
    def symbol(self):
        return '♖' if self.color == 'white' else '♜'

    def valid_moves(self, current_position, board):
        x, y = current_position
        moves = []

        # Direcciones: arriba, abajo, izquierda, derecha
        directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
        for dx, dy in directions:
            i = 1
            while True:
                nx, ny = x + i * dx, y + i * dy
                if 0 <= nx < 8 and 0 <= ny < 8:
                    if not board[nx][ny]:  # Casilla vacía
                        moves.append((nx, ny))
                    else:
                        if board[nx][ny].color != self.color:  # Pieza oponente
                            moves.append((nx, ny))
                        break  # No podemos pasar por encima de otras piezas
                    i += 1
                else:
                    break

        return moves

# Knight (Caballo)
class Knight(Piece):
    def symbol(self):
        return '♘' if self.color == 'white' else '♞'

    def valid_moves(self, current_position, board):
        x, y = current_position
        moves = []

        jumps = [(1, 2), (2, 1), (-1, 2), (-2, 1), (1, -2), (2, -1), (-1, -2), (-2, -1)]
        for dx, dy in jumps:
            nx, ny = x + dx, y + dy
            if 0 <= nx < 8 and 0 <= ny < 8 and (not board[nx][ny] or board[nx][ny].color != self.color):
                moves.append((nx, ny))

        return moves
    
# Bishop (Alfil)
class Bishop(Piece):
    def symbol(self):
        return '♗' if self.color == 'white' else '♝'

    def valid_moves(self, current_position, board):
        x, y = current_position
        moves = []

        # Direcciones diagonales
        directions = [(-1, -1), (-1, 1), (1, -1), (1, 1)]
        for dx, dy in directions:
            i = 1
            while True:
                nx, ny = x + i * dx, y + i * dy
                if 0 <= nx < 8 and 0 <= ny < 8:
                    if not board[nx][ny]:
                        moves.append((nx, ny))
                    else:
                        if board[nx][ny].color != self.color:
                            moves.append((nx, ny))
                        break
                    i += 1
                else:
                    break

        return moves

# Queen (Reina)
class Queen(Piece):
    def symbol(self):
        return '♕' if self.color == 'white' else '♛'

    def valid_moves(self, current_position, board):
        # Reutilizamos la lógica de Rook y Bishop para obtener sus movimientos
        return Rook.valid_moves(self, current_position, board) + Bishop.valid_moves(self, current_position, board)

# King (Rey)
class King(Piece):
    def symbol(self):
        return '♔' if self.color == 'white' else '♚'

    def valid_moves(self, current_position, board):
        x, y = current_position
        moves = []

        steps = [-1, 0, 1]
        for dx in steps:
            for dy in steps:
                if dx == 0 and dy == 0:
                    continue
                nx, ny = x + dx, y + dy
                if 0 <= nx < 8 and 0 <= ny < 8 and (not board[nx][ny] or board[nx][ny].color != self.color):
                    moves.append((nx, ny))

        return moves

# La clase Chessboard (Tablero de ajedrez)
class Chessboard:
    def __init__(self):
        self.board = [['' for _ in range(8)] for _ in range(8)]
        self.initialize_pieces()

    def initialize_pieces(self):
        # Piezas negras (top del tablero)
        for i in range(8):
            self.board[1][i] = Pawn('black')
        self.board[0][0] = Rook('black')
        self.board[0][1] = Knight('black')
        self.board[0][2] = Bishop('black')
        self.board[0][3] = Queen('black')
        self.board[0][4] = King('black')
        self.board[0][5] = Bishop('black')
        self.board[0][6] = Knight('black')
        self.board[0][7] = Rook('black')

        # Piezas blancas (bottom del tablero)
        for i in range(8):
            self.board[6][i] = Pawn('white')
        self.board[7][0] = Rook('white')
        self.board[7][1] = Knight('white')
        self.board[7][2] = Bishop('white')
        self.board[7][3] = Queen('white')
        self.board[7][4] = King('white')
        self.board[7][5] = Bishop('white')
        self.board[7][6] = Knight('white')
        self.board[7][7] = Rook('white')

    def move_piece(self, start, end):
        x1, y1 = start
        x2, y2 = end
        piece = self.board[x1][y1]
        
        if not piece:
            return False, "No hay ninguna pieza en la posición inicial."

        valid_moves = piece.valid_moves(start, self.board)
        if end in valid_moves:
            # Movemos la pieza a la nueva posición
            self.board[x2][y2] = piece
            # Vaciamos la posición inicial
            self.board[x1][y1] = ''
            return True, "Movimiento exitoso."
        else:
            return False, "Movimiento no válido."

class Game:
    def __init__(self):
        self.board = Chessboard()
        self.turn = 'white'

    def move(self, start, end):
        success, message = self.board.move_piece(start, end)
        if success:
            self.switch_turn()
        return success, message

    def switch_turn(self):
        self.turn = 'black' if self.turn == 'white' else 'white'

game = Game()

@app.route('/')
def index():
    return render_template('index.html', board=game.board.board)

@app.route('/move', methods=['POST'])
def move():
    data = request.json
    start = tuple(data['start'])
    end = tuple(data['end'])
    success, message = game.move(start, end)
    return jsonify({"success": success, "message": message})

if __name__ == "__main__":
    app.run(debug=True)