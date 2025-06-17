#include <stdio.h>

#include "../include/part1.h"
#include "../include/part2.h"

int main(void) {
  char file_name[50] = "../data/puzzle_input.txt";
  // char file_name[50] = "../data/part1_sample.txt";

  // 2632
  long int sum_ids = FindSumOfGamesId(file_name);

  // 69629
  long int powers_sum = FindSumOfGamesPower(file_name);

  printf("\nThe Sum is: %ld\n", sum_ids);
  printf("The sum of power: %ld\n", powers_sum);
  return 0;
}