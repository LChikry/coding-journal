#include <stdio.h>
#include <string.h>
#include <stdlib.h>

#include "../include/common.h"

 int FindSumOfGamesPower(char *file_name) {
  FILE *file_pointer = fopen(file_name, "r");
  if (file_pointer == NULL) {
    puts("the file doesn't exist");
    exit(1);
  }

  long int min_reds = 0, min_blues = 0, min_greens = 0;
  long int set_power = 0, power_sum = 0;
  long int number_holder, blue_cubes = 0, red_cubes = 0, green_cubes = 0;
  char *line_pointer = NULL;
  char line[CHAR_SIZE];
  char *game_set = NULL;
  char *name_holder = NULL;

  // lines in the file iteration
  while (fgets(line, CHAR_SIZE, file_pointer) != NULL) {
    line_pointer = line;
    (void)strtok_r(line_pointer, " ", &line_pointer);
    number_holder = strtol(line_pointer, &line_pointer, 10);
    (void)strtok_r(line_pointer, " ", &line_pointer);

    min_reds = 0, min_blues = 0, min_greens = 0;
    // game iteration
    while ((game_set = strtok_r(line_pointer, ";", &line_pointer)) != NULL) {
      blue_cubes = 0, red_cubes = 0, green_cubes = 0;
      // set iteration
      while (game_set != NULL) {
        number_holder = strtol(game_set, &game_set, 10);
        name_holder = strtok_r(game_set, ",;", &game_set);

        if (GREEN == WhatColor(name_holder)) green_cubes = number_holder;
        if (RED == WhatColor(name_holder)) red_cubes = number_holder;
        if (BLUE == WhatColor(name_holder)) blue_cubes = number_holder;
      }  // while of the set

      // check the result of each set
      if (green_cubes > min_greens) min_greens = green_cubes;
      if (red_cubes > min_reds) min_reds = red_cubes;
      if (blue_cubes > min_blues) min_blues = blue_cubes;
    }  // while of the whole game

    set_power = min_blues * min_greens * min_reds;
    power_sum += set_power;
  }  // end of while that iterates on the file

  fclose(file_pointer);
  return power_sum;
}