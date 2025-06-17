#include <stdio.h>

// 26ELD7

#include "../include/part1.h"
#include "../include/part2.h"

int main(void) {
  char file_name[50] = "../data/puzzle_input.txt";

  int sum = AddFirstAndLastNumberInAString(file_name);
  printf("Sum of first part is %d\n", sum);

  printf("Sum of second part is %d\n", sum);
  sum = EffectiveNumberAddition(file_name);

  return 0;
}