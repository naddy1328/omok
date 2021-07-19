#include <stdio.h>
#include <windows.h>

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
CheckUnit check_units[20];
char ally;
char enemy;
int in_a_row_counter[4][5];
int largest_each_direction[4];
bool over_five_flag;

void initBoard();
void showBoard();
void playStone();
bool isValidInput(Pos pos);
void makeCheckUnits(Pos pos);
void showCheckUnits();
bool isBannedPlay();
bool isWin();

// const
Pos HORI = { 1, 0 };
Pos VERT = { 0, 1 };
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
			makeCheckUnits(pos);
			showCheckUnits();
			if (isWin()) {
				char winner = (turn == 1) ? 'O' : 'X';
				board[pos.y][pos.x] = (turn == 1) ? 'b' : 'w';
				showBoard();
				printf("GAME OVER, %c가 승리했습니다\n", winner);
				system("PAUSE");
				initBoard();
				break;
			}

			if (isBannedPlay()) {
				printf("쌍삼입니다\n");
				continue;
			}
			//착수
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

void makeCheckUnits(Pos pos) {
	Pos direction[4] = { HORI, VERT, DIAG, R_DIAG };

	int result_idx = 0;
	for (int d = 0; d < 4; d++) {
		for (int i = -2; i < 3; i++) {
			check_units[result_idx].init_pos = { pos.x + i * direction[d].x , pos.y + i * direction[d].y };
			check_units[result_idx].start_idx = 2 - i;
			for (int img = -2; img < 3; img++) {
				int x, y;
				x = check_units[result_idx].init_pos.x + img * direction[d].x;
				y = check_units[result_idx].init_pos.y + img * direction[d].y;
				if (0 <= x && x < 15 && 0 <= y && y < 15) {
					check_units[result_idx].img[img + 2] = board[y][x];
				}
				else {
					check_units[result_idx].img[img + 2] = 'x'; // 배열 범위 벗어남
				}
			}
			check_units[result_idx].img[5] = '\0';
			check_units[result_idx].direction = direction[d];
			result_idx++;
		}
	}

	char ally = (turn == 1) ? 'b' : 'w';
	char enemy = (turn == -1) ? 'b' : 'w';

	// 중간에 적 돌이 낄 경우에 대한 처리
	for (int d = 0; d < 4; d++) { // d is direction		
		for (int i = 0; i < 5; i++) { // i is index
			for (int img = 0; img < 5; img++) {
				if (img == enemy) {
					if (i < check_units[d * 5 + i].start_idx) {
						for (int j = 0; j <= i; j++) {
							check_units[d * 5 + i].img[j] = '*';
						}
					}
					else {
						for (int j = 4; j >= i; j--) {
							check_units[d * 5 + i].img[j] = '*';
						}
					}
				}
			}
		}
	}
	for (int d = 0; d < 4; d++) {
		for (int i = 0; i < 5; i++) {
			int count = 0;
			for (int img = 0; img < 5; img++) {
				if (check_units[d * 5 + i].img[img] == ally) {
					count++;
				}
			}
			in_a_row_counter[d][i] = count;
		}
	}

	over_five_flag = false;
	for (int d = 0; d < 4; d++) {
		int val = 0;
		for (int i = 0; i < 5; i++) {
			if (in_a_row_counter[d][i] > val) {
				val = in_a_row_counter[d][i];
				if (val == 4) {
					int x, y;
					x = check_units[d * 5 + i].init_pos.x - 3 * check_units[d * 5 + i].direction.x;
					y = check_units[d * 5 + i].init_pos.y - 3 * check_units[d * 5 + i].direction.y;
					if (0 <= x && x < 15 && 0 <= y && y < 15 && board[y][x] == ally) {over_five_flag = true;}
					x = check_units[d * 5 + i].init_pos.x + 3 * check_units[d * 5 + i].direction.x;
					y = check_units[d * 5 + i].init_pos.y + 3 * check_units[d * 5 + i].direction.y;
					if (0 <= x && x < 15 && 0 <= y && y < 15 && board[y][x] == ally) { over_five_flag = true; }
				}
			}
		}
		largest_each_direction[d] = val;
	}
}

void showCheckUnits() {
	for (int i = 0; i < 20; i++) {
		printf(".init_pos:[%d, %d], start_idx: %d, img: %s, directions:[%d %d]\n"
			,check_units[i].init_pos.x, check_units[i].init_pos.y, check_units[i].start_idx, check_units[i].img, check_units[i].direction.x, check_units[i].direction.y);
	}
}

bool isBannedPlay() {
	// 본 함수는 makeCheckUnits() 함수에 의존적입니다
	int three_counter = 0;
	for (int i = 0; i < 4; i++) {
		if (largest_each_direction[i] == 2) {
			three_counter++;
		}
	}

	if (three_counter >= 2) {
		return true;
	}

	return false;
}

bool isWin() {
	int five_counter = 0;
	for (int i = 0; i < 4; i++) {
		if (largest_each_direction[i] == 4) {
			five_counter++;
		}
	}
	if (!(over_five_flag)&&five_counter != 0) {
		return true;
	}
	return false;
}

