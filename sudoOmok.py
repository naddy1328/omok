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

    # 방향을 정해줌
    HORI = Pos(1, 0)
    VERT = Pos(0, 1)
    DIAG = Pos(1, 1)
    R_DIAG = Pos(1, -1)

    PosInfo = namedtuple('PosInfo', 'x y direction')
    dots = [PosInfo(pos.x + i * direction.x, pos.y + i * direction.y, direction) for direction in [HORI, VERT, DIAG, R_DIAG] for i in range(-2, 3)]
    def checker(pos:PosInfo) -> list:
        line = ''
        for i in range(-2, 3):
            if 0 <= pos.y + i * pos.direction.y < 15 and 0 <= pos.x + i * pos.direction.x < 15:
                obj_in_location = board[pos.y + i * pos.direction.y][pos.x + i * pos.direction.x]
                line += obj_in_location
        return line

    result = []
    ImgInfo = namedtuple('ImgInfo', 'init_pos, img direction')
    for dot in dots:
        print(dot)
        result += [dot, checker(dot), dot.direction]
    pprint(result)
    # TODO 이제 대충 금수인지 아닌지 확인하시오
    
    
        
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





