from abc import ABC, abstractmethod
import random
class Difficulty(ABC):
    @abstractmethod
    def play(self, board, pc):
        pass

class Easy(Difficulty):
    @staticmethod
    def random_empty_cell(board):
        empty_cells = []
        for i in range(len(board)):
            for j in range(len(board[0])):
                if board[i][j] == 0:
                    empty_cells.append((i, j))

        if empty_cells:
            x, y = random.choice(empty_cells)
            return x, y  
        else:
            return None, None  

    def play(self, board, pc):
        pc.Decrement_Disks()
        x, y = Easy.random_empty_cell(board)
        return x , y






class Medium(Difficulty):
    def play(self, board, pc):
        print(f"Medium difficulty: playing with moderate challenge. pc: {pc}")
        pc.Decrement_Disks()


class Hard(Difficulty):
    def play(self, board, pc):
        print(f"Hard difficulty: playing with high challenge. pc: {pc}")
        pc.Decrement_Disks()


class DifficultyFactory:
    @staticmethod
    def create_difficulty(level):
        if level == "easy":
            return Easy()
        elif level == "medium":
            return Medium()
        elif level == "hard":
            return Hard()
        else:
            raise ValueError("Invalid difficulty level")
