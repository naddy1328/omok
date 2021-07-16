from pprint import pprint
from copy import deepcopy
from collections import namedtuple
import os

BLACK = '●'
WHITE = '○'
turn = 1
board = [["+" for _ in range(15)] for __ in range(15)]

def showBoard():
    for i, line in enumerate(board):
        print("  ".join(line))
    print("="*30)

def playStone(x: int, y: int):
    global turn
    board[y][x] = BLACK if turn == 1 else WHITE
    turn *= -1

def choosePlay() -> list:
    while True:
        print("착수지점: ", end='')
        pos = input().split()
        if isValidInput(pos):
            return list(map(int, pos))
            
def isValidInput(pos: str) -> bool:    
    # 입력한 착수 지점의 형식이 올바른지 확인
    # TODO DEBUG 예외

    # 입력값이 2개가 아닌 경우를 확인
    rule_input_two = lambda x: len(x) != 2
    if rule_input_two(pos):
        print("2개의 숫자를 입력해야 합니다(0~14)")
        return False
    
    # 입력값이 범위를 벗아남
    RANGE = [str(i) for i in range(15)]
    rule_range_out = lambda x: (x[0] not in RANGE) or (x[1] not in RANGE)
    if rule_range_out(pos):
        print("0~14 사이의 숫자를 입력해야 합니다")
        return False
    
    # 빈 곳에 착수해야함
    rule_only_empty = lambda x: board[int(x[1])][int(x[0])] != '+'
    if rule_only_empty(pos):
        print("해당 위치에는 이미 돌이 존재합니다")
        return False

    return True

def isBannedLocation(_pos: list) -> bool:
    Pos = namedtuple('Pos', 'x y')
    pos = Pos(_pos[0], _pos[1])
    HORI = Pos(0, 1)
    VERT = Pos(1, 0)
    DIAG = Pos(1, 1)
    R_DIAG = Pos(1, -1)

    pos_lists = [[[pos.y + i * direction.y, pos.x + i * direction.x, direction] for i in range(-2, 3)] for direction in [HORI, VERT, DIAG, R_DIAG]]
    pprint(pos_lists)

    def checkHori():
        pass
    def checkVert():
        pass
    def checkDiag():
        pass
    def checkReverseDiag():
        pass
        
    # 입력한 착수 지점이 금수에 해당하는지 확인
        # hori, vert, diag, rDiag
        # 입력 값이 쌍삼임
        # 입력 값이 뜬삼임
        # 입력 값이 뜬뜬삼임
    pass

def isWin():
    # 오목 완성 여부 확인(6목 제외)
    pass

if __name__ == '__main__':
    os.system('cls')
    isBannedLocation([0, 0])
    while True:
        showBoard()
        choosePlay()





