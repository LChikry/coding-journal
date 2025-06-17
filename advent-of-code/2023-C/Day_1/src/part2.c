#include <ctype.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#include "../include/common.h"

int EffectiveNumberAddition(char *file_name) {
  FILE *pointer_to_file = fopen(file_name, "r");
  if (pointer_to_file == NULL) {
    puts("test_input.txt file didn't open");
    exit(1);
  }

  int sum = 0;
  char line[CHAR_SIZE];
  while (fgets(line, CHAR_SIZE, pointer_to_file) != NULL) {
    int first_digit = -1, last_digit = -1, character_counter = -1,
        possible_digit;
    char front_digit_name[CHAR_SIZE] = {'\0'};
    char rear_digit_name[CHAR_SIZE] = {'\0'};

    int length = strlen(line);

    for (int i = 0; i <= length; i++) {
      if (isdigit(line[i])) {
        WriteTheNumber(&first_digit, &last_digit, line[i] - '0');
        break;
      }

      snprintf(&front_digit_name[++character_counter], CHAR_SIZE, "%c",
               line[i]);
      if (i < 2) continue;
      possible_digit = DigitNameRecognition(front_digit_name);
      if (possible_digit == -1) continue;
      WriteTheNumber(&first_digit, &last_digit, possible_digit);
      break;
    }

    character_counter = -1;
    for (int i = length - 1; i >= 0; i--) {
      if (isdigit(line[i])) {
        WriteTheNumber(&first_digit, &last_digit, line[i] - '0');
        break;
      }

      snprintf(&rear_digit_name[++character_counter], CHAR_SIZE, "%c", line[i]);
      if (i >= length - 2) continue;
      possible_digit = ReverseDigitNameRecognition(rear_digit_name);
      if (possible_digit == -1) continue;
      WriteTheNumber(&first_digit, &last_digit, possible_digit);
      break;
    }

    if (first_digit == -1 || last_digit == -1) {
      puts("digits didn't change");
      exit(1);
    }

    sum = sum + last_digit + first_digit;

  }  // end of while loop
  fclose(pointer_to_file);
  return sum;
}

int LessEffectiveNumberAddition(char *file_name) {
  FILE *pointer_to_file = fopen(file_name, "r");
  if (pointer_to_file == NULL) {
    puts("file didn't open in AddFirstAndLastNumberInString function");
    exit(1);
  }

  int sum = 0;
  char line[CHAR_SIZE];
  while (fgets(line, CHAR_SIZE, pointer_to_file) != NULL) {
    int first_digit = -1, last_digit = -1, character_counter = -1;
    int iteration_start_point = 0, possible_digit;
    char digit_name[CHAR_SIZE] = {'\0'};

    int length = strlen(line);
    for (int i = 0; i < length; i++) {
      if (isdigit(line[i])) {
        WriteTheNumber(&first_digit, &last_digit, line[i] - '0');
        continue;
      }

      snprintf(&digit_name[++character_counter], CHAR_SIZE, "%c", line[i]);
      if (strlen(&digit_name[iteration_start_point]) <= 2) continue;

      possible_digit = DigitNameRecognition(&digit_name[iteration_start_point]);
      if (possible_digit == -1) continue;

      WriteTheNumber(&first_digit, &last_digit, possible_digit);
      iteration_start_point = character_counter;
    }

    sum = sum + last_digit + first_digit;
  }  // end of while loop

  fclose(pointer_to_file);
  return sum;
}
