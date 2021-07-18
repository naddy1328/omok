from pprint import pprint
from copy import deepcopy
from collections import namedtuple
import os

BLACK = '●'
WHITE = '○'
turn = 1
board = [["+" for _ in range(15)] for __ in range(15)]

debug = False

def showBoard():
    print("   " + "  ".join([str(i)[-1] for i in range(15)]))
    for i, line in enumerate(board):
        print(str(i)[-1] + "  " + "  ".join(line))
    print("="*30)

def choosePlay() -> list:
    while True:
        print("착수지점: ", end='')
        pos = input().split()
        if isValidInput(pos):
            pos = list(map(int, pos[0:2]))
            global debug
            if debug:
                playStone(pos[0], pos[1])
                debug = False
                return
            scan_lines = scanLines(pos)
            if isWin(scan_lines):
                print(BLACK if turn == 1 else WHITE, "is win.")
                input()
                global board
                board = [["+" for _ in range(15)] for __ in range(15)]
                return
            if isBannedLocation(scan_lines):
                continue
            playStone(pos[0], pos[1])
            return

def playStone(x: int, y: int):
    global turn
    board[y][x] = BLACK if turn == 1 else WHITE
    turn *= -1
            
def isValidInput(pos: list) -> bool:    
    # 입력한 착수 지점의 형식이 올바른지 확인
    # TODO DEBUG 예외
    rule_DEBUG = lambda x: len(x) == 3 and x[2].lower() in ['b', 'w'] 
    if rule_DEBUG(pos):
        global debug
        global turn
        debug = True
        turn = 1 if pos[2] == 'b' else -1
        return True

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

def scanLines(_pos: list) -> bool:
    Pos = namedtuple('Pos', 'x y')
    pos = Pos(_pos[0], _pos[1])

    # 방향을 정해줌
    HORI = Pos(1, 0)
    VERT = Pos(0, 1)
    DIAG = Pos(1, 1)
    R_DIAG = Pos(1, -1)

    PosInfo = namedtuple('PosInfo', 'x y direction idx')
    dots = [PosInfo(pos.x + i * direction.x, pos.y + i * direction.y, direction, 3-i) for direction in [HORI, VERT, DIAG, R_DIAG] for i in range(-2, 3)]
    def checker(pos:PosInfo) -> list:
        line = ''
        for i in range(-2, 3):
            if 0 <= pos.y + i * pos.direction.y < 15 and 0 <= pos.x + i * pos.direction.x < 15:
                obj_in_location = board[pos.y + i * pos.direction.y][pos.x + i * pos.direction.x]
                line += obj_in_location
            else:
                line += 'x'
        return line

    result = []
    ImgInfo = namedtuple('ImgInfo', 'init_pos img direction idx')
    for dot in dots:
        result += [ImgInfo(Pos(dot.x, dot.y), checker(dot), dot.direction, dot.idx)]



    for _i, r in enumerate(result):
        ally_color = BLACK if turn == 1 else WHITE
        enemy_color = WHITE if turn == 1 else BLACK
        for i, d in enumerate(r.img):
            if d == enemy_color:
                tmp_img = "*" * (i+1) + r.img[i+1:] if i < r.idx else r.img[:i] + "*" * (5-i)
                result[_i] = ImgInfo(Pos(r.init_pos.x, r.init_pos.y), tmp_img, r.direction, r.idx)
            # d를 검사해서 반대색 돌이 깔려있으면 다음과 같이 동작한다
            # ㄴ 1. i가 r.idx보다 작다면 이전까지의 내용을 지운다
            # ㄴ 2. i가 r.idx보다 크다면 이후의 내용을 모두 지운다
            # ㄴ 착수위치는 돌이 없으므로 i는 r.idx보다 크거나 작다
    return result

def isBannedLocation(scan_lines: list) -> bool:
    ally_color = BLACK if turn == 1 else WHITE
    enemy_color = WHITE if turn == 1 else BLACK
    Pos = namedtuple('Pos', 'x y')
    # 방향을 정해줌
    HORI = Pos(1, 0)
    VERT = Pos(0, 1)
    DIAG = Pos(1, 1)
    R_DIAG = Pos(1, -1)

    judge = dict()
    for direction in [HORI, VERT, DIAG, R_DIAG]:
        judge[direction] = 0
    for _i, r in enumerate(scan_lines):
        if len(r.img.replace('x', '').replace("*", '')) >= 3:
            judge[r.direction] = max(judge[r.direction], r.img.count(ally_color))

    num_of_three = 0
    for k in judge.keys():
        if judge[k] == 2:
            num_of_three += 1
    print("num_of_three:", num_of_three)
    print(judge)
    if num_of_three >= 2:
        print("쌍삼입니다")
        return True
    return False

def isWin(scan_lines: list) -> bool:
    Pos = namedtuple('Pos', 'x y')
    # 방향을 정해줌
    HORI = Pos(1, 0)
    VERT = Pos(0, 1)
    DIAG = Pos(1, 1)
    R_DIAG = Pos(1, -1)

    judge = dict()
    for direction in [HORI, VERT, DIAG, R_DIAG]:
        judge[direction] = 0
    for _i, r in enumerate(scan_lines):
        if len(r.img.replace('x', '').replace("*", '').replace('+', '')) >= 4:
            return True

if __name__ == '__main__':
    os.system('cls')
    while True:
        showBoard()
        choosePlay()





