from pprint import pprint
from copy import deepcopy
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

def choosePlay():
    while True:
        print("착수지점: ", end='')
        rule_input_two = lambda x: len(x) != 2
        RANGE = [str(i) for i in range(15)]
        rule_range_out = lambda x: (x[0] not in RANGE) or (x[1] not in RANGE)
        try:
            pos = input().split()
            if rule_input_two(pos):
                print("숫자 2개 입력하셈")
                continue
            pos = list(map(int, pos.split()))
            return pos
        except:
            if rule_range_out(pos):
                print("0~14까지의 숫자만 입력할 수 있음")
                continue
            
def isInvalidInput():    
    # 입력한 착수 지점의 형식이 올바른지 확인
        # DEBUG 예외
        # 입력값이 2개가 아님
        # 입력값이 범위를 벗아남
    pass

def isBannedLocation():
    # 입력한 착수 지점이 금수에 해당하는지 확인
        # 입력 값이 쌍삼임
        # 입력 값이 뜬삼임
        # 입력 값이 뜬뜬삼임
    pass

if __name__ == '__main__':
    os.system('cls')
    showBoard()
    choosePlay()





