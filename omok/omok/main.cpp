#include <stdio.h>

struct Pos {
	int x;
	int y;
};
struct CheckUnit {
	Pos init_pos;
	int start_idx;
	char img[6];
	Pos direction;
};

// 전역변수
char board[15][15];
int turn = 1;

void initBoard();
void showBoard();
void playStone();
bool isValidInput(Pos pos);
void showCheckUnits(CheckUnit* units);
CheckUnit* makeCheckUnits(Pos pos);

// const
Pos VERT = { 0, 1 };
Pos HORI = { 1, 0 };
Pos DIAG = { 1, 1 };
Pos R_DIAG = { 1, -1 };
char BLACK = 'O';
char WHITE = 'X';


/* START MAIN */
int main() {
	initBoard();
	while (true)
	{
		showBoard();
		playStone();
	}

}

void initBoard() {
	for (int i = 0; i < 15; i++) {
		for (int j = 0; j < 15; j++) {
			board[j][i] = '+';
		}
	}
}

void showBoard() {
	// show horizontal index
	printf("  0 1 2 3 4 5 6 7 8 9 0 1 2 3 4\n");

	// show board with vertical index
	for (int i = 0; i < 15; i++) {
		printf("%d", i % 10);
		for (int j = 0; j < 15; j++) {
			printf (" ");
			switch (board[i][j])
			{
			case 'b':
				printf("%c", BLACK);
				break;
			case 'w':
				printf("%c", WHITE);
				break;
			case '+':
				printf("%s", "┼");
				break;
			default:
				break;
			}
		}
		printf("\n");
	}
}

void playStone() {
	while (true)
	{
		int x, y;
		scanf_s("%d %d", &x, &y);
	
		Pos pos = { x, y };
		if (isValidInput(pos)) {
			CheckUnit* units = makeCheckUnits(pos);
			showCheckUnits(units);
			board[pos.y][pos.x] = (turn == 1) ? 'b':'w';
			turn *= -1;
			break;
		}
	}
}

bool isValidInput(Pos pos) {
	// 0 <= x, y < 15 and 0 
	if (0 <= pos.x && pos.x < 15 && 0 <= pos.y && pos.y < 15){
		if (board[pos.y][pos.x] != '+') {
			printf("해당 위치에 이미 돌이 존재하여 착수가 불가합니다\n");
		}
		return true;
	}
	else {
		printf("0~14 범위의 숫자를 2개 입력하십시오\n");
		return false;
	}
}

CheckUnit* makeCheckUnits(Pos pos) {
	CheckUnit result[20];
	Pos direction[4] = { HORI, VERT, DIAG, R_DIAG };

	int result_idx = 0;
	for (int d = 0; d < 4; d++) {
		for (int i = -2; i < 3; i++) {
			result[result_idx].init_pos = { pos.x + i * direction[d].x , pos.y + i * direction[d].y };
			result[result_idx].start_idx = 2 - i;
			for (int img = -2; img < 3; img++) {
				int x, y;
				x = result[result_idx].init_pos.x + img * direction[d].x;
				y = result[result_idx].init_pos.y + img * direction[d].y;
				if (0 <= x && x < 15 && 0 <= y && y < 15) {
					result[result_idx].img[img + 2] = board[y][x];
				}
				else {
					result[result_idx].img[img + 2] = 'x'; // 배열 범위 벗어남
				}
			}
			result[result_idx].img[5] = '\0';
			result[result_idx].direction = direction[d];
			result_idx++;
		}
	}

	return result;
}

void showCheckUnits(CheckUnit *units) {
	for (int i = 0; i < 20; i++) {
		printf(".init_pos:[%d, %d], start_idx: %d, img: %s, directions:[%d %d]\n", units[i].init_pos.x, units[i].init_pos.y, units[i].start_idx, units[i].img, units[i].direction.x, units[i].direction.y);
	}
}