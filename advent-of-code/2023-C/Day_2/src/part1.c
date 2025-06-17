#include <stdio.h>
#include <string.h>
#include <stdlib.h>

#include "../include/common.h"

int FindSumOfGamesId(char *file_name) {
  FILE *file_pointer = fopen(file_name, "r");
  if (file_pointer == NULL) {
    puts("the file doesn't exist");
    exit(1);
  }

  long int game_id, sum_ids = 0, number_holder, blue_cubes = 0, red_cubes = 0,
                    green_cubes = 0;
  char *line_pointer = NULL;
  char line[CHAR_SIZE];
  char *game_set = NULL;
  char *name_holder = NULL;

  while (fgets(line, CHAR_SIZE, file_pointer)) {
    line_pointer = line;
    (void)strtok_r(line_pointer, " ", &line_pointer);
    game_id = strtol(line_pointer, &line_pointer, 10);
    (void)strtok_r(line_pointer, " ", &line_pointer);

    while ((game_set = strtok_r(line_pointer, ";", &line_pointer)) != NULL) {
      blue_cubes = 0, red_cubes = 0, green_cubes = 0;
      while (game_set != NULL) {
        number_holder = strtol(game_set, &game_set, 10);
        name_holder = strtok_r(game_set, ",;", &game_set);

        if (GREEN == WhatColor(name_holder)) green_cubes = number_holder;
        if (RED == WhatColor(name_holder)) red_cubes = number_holder;
        if (BLUE == WhatColor(name_holder)) blue_cubes = number_holder;
      }  // while of the set

      // check the result of each set
      if (green_cubes > MAX_GREEN || blue_cubes > MAX_BLUE ||
          red_cubes > MAX_RED) {
        game_id = 0;
        break;  // if one set is bad, the whole game is bad
      }
    }  // while of the whole game

    sum_ids += game_id;
  }  // end of while that iterates on the file

  fclose(file_pointer);

  return sum_ids;
}