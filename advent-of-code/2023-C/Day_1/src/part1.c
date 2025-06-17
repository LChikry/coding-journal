#include <ctype.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#include "../include/common.h"

size_t AddFirstAndLastNumberInAString(char *file_name) {
  FILE *pointer_to_file = fopen(file_name, "r");
  if (pointer_to_file == NULL) {
    puts("test_input.txt file didn't open");
    exit(1);
  }

  size_t sum = 0;
  char line[CHAR_SIZE];
  while (fgets(line, CHAR_SIZE, pointer_to_file)) {
    size_t first_digit = -1, last_digit = -1;
    size_t length = strlen(line);

    for (size_t i = 0; i < length; ++i) {
      if (isdigit(line[i])) {
        WriteTheNumber(&first_digit, &last_digit, line[i] - '0');
      }
    }

    sum = sum + first_digit + last_digit;
  }

  fclose(pointer_to_file);
  return sum;
}