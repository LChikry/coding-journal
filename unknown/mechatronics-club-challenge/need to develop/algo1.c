#include <stdbool.h>
#include <stdio.h>
#include <string.h>


bool isPositionReachedV1(int x_final, int y_final, const char *instructions) {
  int x_initial = 0, y_initial = 0;  // starting point

  int num_instructions = strlen(instructions);

  while (x_initial < x_final && y_initial < y_final) {
    for (int i = 0; i < num_instructions; i++) {
      switch (instructions[i]) {
        case 'U':
          y_initial++;
          break;

        case 'D':
          y_initial--;
          break;

        case 'R':
          x_initial++;
          break;

        case 'L':
          x_initial--;
          break;

        default:
          printf("the instructions are false.\n");
          break;
      }
    }
  }

  if (x_initial == x_final && y_initial == y_final) return 1;

  return 0;
}

int main(void) { isPositionReachedV1(); }