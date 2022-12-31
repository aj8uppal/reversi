import numpy as np


class ReversiSolver:
    BOARD_WIDTH = 8

    def __init__(self) -> None:
        self.board = np.zeros((self.BOARD_WIDTH, self.BOARD_WIDTH))
        self.board[self.BOARD_WIDTH // 2 - 1, self.BOARD_WIDTH // 2 - 1] = 1
        self.board[self.BOARD_WIDTH // 2 - 1, self.BOARD_WIDTH // 2] = 2
        self.board[self.BOARD_WIDTH // 2, self.BOARD_WIDTH // 2 - 1] = 2
        self.board[self.BOARD_WIDTH // 2, self.BOARD_WIDTH // 2] = 1
        self.BLACK = 2  # DEFAULT AI
        self.WHITE = 1  # DEFAULT HUMAN
        self.states = {
            self.BLACK: {},
            self.WHITE: {},
        }
        self.update_states()

    def move(self, move: tuple[int, int], color: int, respond_with_move: bool = True) -> None:
        assert color in (self.WHITE, self.BLACK)
        self.flip(move, color)
        if respond_with_move:
            return self.compute_ai_move(3 - color)

    def flip(self, move: tuple[int, int], color: int):
        if move not in (state := self.states[color]):
            return False
        # TODO: is there a better way to update 2d array board with multiple coordinates vectorized? hmm or at least better than nested array?
        # breakpoint()
        for dir in state[move].values():
            for coord in dir:
                self.board[coord] = color
        self.board[tuple(move)] = color
        self.update_states()


    def update_states(self):
        rows, cols = self.board.shape
        for x in range(rows):
            for y in range(cols):
                if not self.board[(x, y)]:
                    self.precompute_flips(x, y)
                else:
                    if (x, y) in self.states[self.WHITE]:
                        del self.states[self.WHITE][(x, y)]
                    if (x, y) in self.states[self.BLACK]:
                        del self.states[self.BLACK][(x, y)]

    def precompute_flips(self, x: int, y: int):
        directions = [(0, 1), (1, 1), (1, 0), (1, -1), (0, -1), (-1, -1), (-1, 0), (-1, 1)]
        self.states[self.WHITE][(x, y)] = {}
        self.states[self.BLACK][(x, y)] = {}
        for dx, dy in directions:
            # if (x, y) == (4, 2) and (dx, dy) == (-1, 1):
            #     breakpoint()
            xf, yf = x+dx, y+dy
            if (0 <= xf < self.BOARD_WIDTH and 0 <= yf < self.BOARD_WIDTH) and (adj_color := self.board[(xf, yf)]):
                coordinate = self.states[3-adj_color][(x, y)]
                while 0 <= xf < self.BOARD_WIDTH and 0 <= yf < self.BOARD_WIDTH and self.board[(xf,yf)] == adj_color:
                    coordinate.setdefault((dx, dy), []).append((xf, yf))
                    xf+=dx
                    yf+=dy
                if (dx, dy) in coordinate and not (0 <= xf < self.BOARD_WIDTH and 0 <= yf < self.BOARD_WIDTH and self.board[(xf, yf)] == 3-adj_color):
                    del coordinate[(dx, dy)]
        # if (x, y) == (4, 2):
        #     breakpoint()
        # if (x, y) == ()
        if not self.states[self.WHITE][(x, y)]:
            del self.states[self.WHITE][(x, y)]
        if not self.states[self.BLACK][(x, y)]:
            del self.states[self.BLACK][(x, y)]

    def compute_ai_move(self, ai_color: int):
        if coord := self.states[ai_color]:
            # breakpoint()
            move = list(coord.keys())[0]
            flips = ReversiSolver._jsonify(coord)[str(move)[1:-1].replace(" ", "")]
            self.flip(move, ai_color)
            return move, flips
        return [], []

    def get_states(self):
        return {color: ReversiSolver._jsonify(self.states[color]) for color in self.states}

    @staticmethod
    def _jsonify(state):
        return {
            str(coord)[1:-1].replace(" ", ""): {
                str(dir)[1:-1].replace(" ", ""): state[coord][dir]
                for dir in state[coord]
            }
            for coord in state
        }