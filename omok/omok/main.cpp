#include <stdio.h>

void showBoard();
void initBoard();

char board[15][15];

int main() {
	initBoard();
	showBoard();
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
	printf("   0  1  2  3  4  5  6  7  8  9  0  1  2  3  4\n");

	// show board with vertical index
	for (int i = 0; i < 15; i++) {
		printf("%d", i % 10);
		for (int j = 0; j < 15; j++) {
			printf ("  ");
			printf("%c", board[i][j]);
		}
		printf("\n");
	}
}